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

    add(satellite: Satellite) {
        this.list = [...this.list, satellite];
    }

    remove(name: string) {
        this.list = this.list.filter(s => s.name !== name);
    }

    clear() {
        this.list = [];
    }
}

export const satelliteStore = new SatelliteStore();
