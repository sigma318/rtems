/*
 *  Message Queue Manager
 *
 *
 *  COPYRIGHT (c) 1989-1998.
 *  On-Line Applications Research Corporation (OAR).
 *  Copyright assigned to U.S. Government, 1994.
 *
 *  The license and distribution terms for this file may be
 *  found in the file LICENSE in this distribution or at
 *  http://www.OARcorp.com/rtems/license.html.
 *
 *  $Id$
 */

#include <rtems/system.h>
#include <rtems/score/sysstate.h>
#include <rtems/score/chain.h>
#include <rtems/score/isr.h>
#include <rtems/score/coremsg.h>
#include <rtems/score/object.h>
#include <rtems/score/states.h>
#include <rtems/score/thread.h>
#include <rtems/score/wkspace.h>
#if defined(RTEMS_MULTIPROCESSING)
#include <rtems/score/mpci.h>
#endif
#include <rtems/rtems/status.h>
#include <rtems/rtems/attr.h>
#include <rtems/rtems/message.h>
#include <rtems/rtems/options.h>
#include <rtems/rtems/support.h>

/*PAGE
 *
 *  rtems_message_queue_flush
 *
 *  This directive removes all pending messages from a queue and returns
 *  the number of messages removed.  If no messages were present then
 *  a count of zero is returned.
 *
 *  Input parameters:
 *    id    - queue id
 *    count - return area for count
 *
 *  Output parameters:
 *    count             - number of messages removed ( 0 = empty queue )
 *    RTEMS_SUCCESSFUL - if successful
 *    error code        - if unsuccessful
 */

rtems_status_code rtems_message_queue_flush(
  Objects_Id  id,
  unsigned32 *count
)
{
  register Message_queue_Control *the_message_queue;
  Objects_Locations               location;

  the_message_queue = _Message_queue_Get( id, &location );
  switch ( location ) {
    case OBJECTS_REMOTE:
#if defined(RTEMS_MULTIPROCESSING)
      _Thread_Executing->Wait.return_argument = count;

      return
        _Message_queue_MP_Send_request_packet(
          MESSAGE_QUEUE_MP_FLUSH_REQUEST,
          id,
          0,                               /* buffer not used */
          0,                               /* size */
          0,                               /* option_set not used */
          MPCI_DEFAULT_TIMEOUT
        );
#endif

    case OBJECTS_ERROR:
      return RTEMS_INVALID_ID;

    case OBJECTS_LOCAL:
      *count = _CORE_message_queue_Flush( &the_message_queue->message_queue );
      _Thread_Enable_dispatch();
      return RTEMS_SUCCESSFUL;
  }

  return RTEMS_INTERNAL_ERROR;   /* unreached - only to remove warnings */
}
