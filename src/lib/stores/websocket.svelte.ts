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
                console.log('WebSocket connected');
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

        this.ws = null;
    }
}

export const wsStore = new WebSocketStore();