/* -*- Mode: C; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*- */
/*
 *     Copyright 2010, 2011 Couchbase, Inc.
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 */
#include "internal.h"

static void breakout_vbucket_state_listener(lcb_server_t *server)
{
    if (server->instance->vbucket_state_listener_last) {
        server->instance->vbucket_state_listener =
            server->instance->vbucket_state_listener_last;
        server->instance->vbucket_state_listener_last = NULL;
    }
    server->instance->io->v.v0.delete_timer(server->instance->io,
                                            server->instance->timeout.event);
    lcb_maybe_breakout(server->instance);
}

static void initial_connect_timeout_handler(lcb_socket_t sock,
                                            short which,
                                            void *arg)
{
    lcb_t instance = arg;
    lcb_error_handler(instance, LCB_CONNECT_ERROR,
                      "Could not connect to server within allotted time");

    if (instance->sock != INVALID_SOCKET) {
        /* Do we need to delete the event? */
        instance->io->v.v0.delete_event(instance->io,
                                        instance->sock,
                                        instance->event);
        instance->io->v.v0.close(instance->io, instance->sock);
        instance->sock = INVALID_SOCKET;
    }

    instance->io->v.v0.delete_timer(instance->io, instance->timeout.event);
    instance->timeout.next = 0;
    lcb_maybe_breakout(instance);

    (void)sock;
    (void)which;
    /* Notice we do not re-set the vbucket_state_listener. This is by design,
     * as we are still in the same state, and are just reporting an error
     * back to the user
     */
}

/**
 * Returns non zero if the event loop is running now
 *
 * @param instance the instance to run the event loop for.
 */
LIBCOUCHBASE_API
int lcb_is_waiting(lcb_t instance)
{
    return instance->wait != 0;
}

/**
 * Run the event loop until we've got a response for all of our spooled
 * commands. You should not call this function from within your callbacks.
 *
 * @param instance the instance to run the event loop for.
 *
 * @author Trond Norbye
 */
LIBCOUCHBASE_API
lcb_error_t lcb_wait(lcb_t instance)
{
    if (instance->wait != 0) {
        return instance->last_error;
    }
    /*
     * The API is designed for you to run your own event loop,
     * but should also work if you don't do that.. In order to be
     * able to know when to break out of the event loop, we're setting
     * the wait flag to 1
     */
    instance->last_error = LCB_SUCCESS;
    instance->wait = 1;
    if (instance->vbucket_config == NULL) {
        /* Initial configuration. Set a timer */
        instance->vbucket_state_listener_last =
            instance->vbucket_state_listener;
        instance->vbucket_state_listener = breakout_vbucket_state_listener;

        /* Initial connection timeout */
        instance->io->v.v0.update_timer(instance->io,
                                        instance->timeout.event,
                                        instance->timeout.usec,
                                        instance,
                                        initial_connect_timeout_handler);
    }
    if (instance->vbucket_config == NULL || lcb_has_data_in_buffers(instance)
            || hashset_num_items(instance->timers) > 0) {
        lcb_size_t idx;
        /* update timers on all servers */
        for (idx = 0; idx < instance->nservers; ++idx) {
            lcb_update_server_timer(instance->servers + idx);
        }
        instance->io->v.v0.run_event_loop(instance->io);
    } else {
        instance->wait = 0;
    }

    return instance->last_error;
}

/**
 * Stop event loop
 *
 * @param instance the instance to run the event loop for.
 */
LIBCOUCHBASE_API
void lcb_breakout(lcb_t instance)
{
    if (instance->wait) {
        instance->io->v.v0.stop_event_loop(instance->io);
        instance->wait = 0;
    }
}
