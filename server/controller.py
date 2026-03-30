import threading
from constellation.core.controller import ScriptableController

class MyController(ScriptableController):
    def __init__(self, on_update=None, **kwargs):
        self._on_update = on_update
        self._last_snapshot = {}
        self._lock = threading.Lock()

        super().__init__(**kwargs)

    # This method builds a snapshot of the constellation.
    # Including the name, type, state, and last changed time for each satellite.
    def _build_snapshot(self):
        snapshot = {}
        satellites = self.constellation.satellites
        hb_states = self.heartbeat_states
        hb_changes = self.heartbeat_state_changes
        failed_satellite_names = set(self.get_failed())

        for canonical_name, sat in satellites.items():
            state = hb_states.get(canonical_name, "-")
            state_str = state.name if hasattr(state, "name") else str(state)

            if canonical_name in failed_satellite_names:
                state_str = "DEAD"

            snapshot[canonical_name] = {
                "name": sat._name,
                "type": sat._class_name,
                "state": state_str,
                "last_changed": str(hb_changes.get(canonical_name, "-")),
            }
        return snapshot
    
    # Auto-triggered when a satellite is added
    def _add_satellite(self, service):
        super()._add_satellite(service)
        self._emit() # Emit the changes immediately after a satellite is added

    # Auto-triggered when a satellite is removed
    def _remove_satellite(self, service):
        super()._remove_satellite(service)
        self._emit() # Emit the changes immediately after a satellite is removed

    # Auto-triggered when a heartbeat is received from a satellite
    def _poll_heartbeats(self):
        super()._poll_heartbeats()
        self._emit() # Emit the changes immediately after polling heartbeats

    def _dispatch(self, events):
        if self._on_update:
            self._on_update(events)

    def _emit(self):
        with self._lock:
            current_satellite_list = self._build_snapshot() # Get the current snapshot of the constellation

            # Satellites that are present in the current snapshot but were not in the last snapshot
            new_satellite = set(current_satellite_list) - set(self._last_snapshot)
            
            # Satellites that were present in the last snapshot but are not in the current snapshot
            removed_satellite = set(self._last_snapshot) - set(current_satellite_list)
            
            # Satellites that are present in both snapshots but have different states
            changed_satellite = {
                satellite for satellite in current_satellite_list if satellite in self._last_snapshot and current_satellite_list[satellite] != self._last_snapshot[satellite]
            }

            # If there are no changes, we can skip emitting
            if not new_satellite and not removed_satellite and not changed_satellite:
                return
            
            # Prepare the events to be emitted based on the changes detected
            events = []

            # Emit events for added satellite
            for name in new_satellite:
                events.append({
                    "event": "satellite_added",
                    "data": current_satellite_list[name]
                })

            # Emit events for removed satellite
            for name in removed_satellite:
                satellite_info = self._last_snapshot[name].copy()
                satellite_info["state"] = "DEAD" # Mark the state as "DEAD" for removed satellites
                events.append({
                    "event": "satellite_removed", 
                    "satellite": satellite_info
                })

            # Emit events for changed satellite
            for name in changed_satellite:
                curr_info = current_satellite_list[name]
                prev_state = self._last_snapshot[name]["state"]

                if curr_info["state"] == "DEAD" and prev_state != "DEAD":
                    # Mark the state as "DEAD" for failed satellites
                    events.append({
                        "event": "satellite_failed",
                        "satellite": curr_info,
                        "previous_state": prev_state,
                    })
                    # Emit the failure events to the registered callback
                else:
                    events.append({
                        "event": "satellite_changed",
                        "satellite": curr_info,
                        "previous_state": prev_state,
                    })

            self._last_snapshot = current_satellite_list
            self._dispatch(events) # Emit the events to the registered callback


    # We can send commands to the satellites using the send_command method.
    def send_command(self, canonical_name, cmd, payload=None):
        if payload is None:
            payload = {}

        # The canonical name is expected to be in the format "satellite_type.satellite_name" such as "Sputnik.Device1"
        satellite_type, satellite_name = canonical_name.split(".", 1)

        # Send the command to the satellite and return the response            
        response = self.command(cmd=cmd, sat=satellite_name, satcls=satellite_type, payload=payload)

        return {
            "success": getattr(response, "success", True),
            "message": getattr(response, "msg", None),
            "payload": getattr(response, "payload", None),
            "meta": getattr(response, "meta", None),
            "error": getattr(response, "errmsg", None)
        }
    
    # We can get the details of a specific satellite using the get_satellite_details method.
    def get_satellite_details(self, canonical_name):
        with self._lock:
            return self._last_snapshot.get(canonical_name, None)
    
    # We can get the list of all satellites in the constellation using the get_all_satellites method.
    def get_all_satellites(self):
        with self._lock:
            return list(self._last_snapshot.values())

