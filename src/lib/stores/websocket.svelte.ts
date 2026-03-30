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

                // The first_snapshot data sent when the connection is first established is an object. 
                // However, when a satellite is added or removed, the data sent is an array.

                if (message.type === 'first_snapshot') {
                    satelliteStore.setAll(message.data);
                } else if (message.type === 'command_response') {
                    const name = message.from.split('.')[1];
                    satelliteStore.setLastMessage(name, message.data.message);
                } else if (Array.isArray(message)) {
                    // I will handle the satellite_failed event later.
                    
                    for (const event of message) {
                        if (event.event === 'satellite_added') {
                            satelliteStore.add(event.data);
                        } else if (event.event === 'satellite_changed') {
                            satelliteStore.update(event.satellite);
                        } else if (event.event === 'satellite_removed') {
                            satelliteStore.remove(event.satellite.name);
                        }
                    }
                }
            }
        } catch (error: any) {
            this.error = error || 'Failed to connect to WebSocket';
        }
    }

    sendCommand(cmd: string, target: string, payload?: string) {
        if (!this.ws || !this.isConnected) return;

        const message: Record<string, string> = {
            type: 'send_command',
            cmd: cmd.toLowerCase(),
            target
        };

        if (payload !== undefined) {
            message.payload = payload;
        }

        this.ws.send(JSON.stringify(message));
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