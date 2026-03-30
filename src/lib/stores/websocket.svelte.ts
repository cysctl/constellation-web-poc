import { satelliteStore } from './satellites.svelte';

export class WebSocketStore {
    ws = $state<WebSocket | null>(null);
    isConnected = $state<boolean>(false);
    isConnecting = $state<boolean>(false);
    error = $state<any>(null);

    connect(host: string, port: number) {
        // check if already connected
        if (this.ws) {
            this.ws.close();
        }

        this.isConnecting = true;

        try {
            const url = `ws://${host}:${port}`;
            this.ws = new WebSocket(url);

            // connection successful
            this.ws.onopen = () => {
                this.isConnected = true;
                this.isConnecting = false;
                this.error = null;
                console.log('WebSocket connected');
            }

            // connection failed
            this.ws.onerror = () => {
                this.error = 'Failed to connect to WebSocket';
                this.isConnecting = false;
                this.isConnected = false;
            }

            // connection closed
            this.ws.onclose = () => {
                this.isConnecting = false;
                this.isConnected = false;
            }

            this.ws.onmessage = (event) => {
                const message = JSON.parse(event.data);

                // I only get the initial data from the system. 
                // The interface will not respond if a satellite is added or removed.
                // I will fix this later.
                
                // Add satellite data to store on first snapshot message
                if (message.type === 'first_snapshot') {
                    satelliteStore.setAll(message.data);
                }
            }
        } catch (error: any) {
            this.error = error || 'Failed to connect to WebSocket';
        }
    }


    disconnect() {
        if (this.ws) {
            this.ws.close();
        }

        // reset state
        this.isConnected = false;
        this.ws = null;
        satelliteStore.clear();
    }
}

export const wsStore = new WebSocketStore();