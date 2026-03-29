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

            // I will handle the onmessage event later
            this.ws.onmessage = event => {

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
    }
}

export const wsStore = new WebSocketStore();