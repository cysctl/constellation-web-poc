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

    update(satellite: Satellite) {
        this.list = this.list.map(s => s.name === satellite.name ? satellite : s);
    }

    remove(name: string) {
        this.list = this.list.filter(s => s.name !== name);
    }

    clear() {
        this.list = [];
    }
}

export const satelliteStore = new SatelliteStore();
