export interface Satellite {
    name: string;
    type: string;
    state: string;
    last_changed: string;
}

class SatelliteStore {
    list = $state<Satellite[]>([]);

    setAll(satellites: Satellite[]) {
        this.list = satellites;
    }

    clear() {
        this.list = [];
    }
}

export const satelliteStore = new SatelliteStore();
