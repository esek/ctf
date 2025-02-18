class Terminal {
    #socket;
    #responseListeners;

    constructor(taskId, program) {
        this.program = program;
        this.#socket = new WebSocket("ws://" + window.location.host + '/ws/terminal/' + taskId + '/' + program + '/');
        this.#responseListeners = [];

        this.#socket.onmessage = (e) => this.#handleMessage(e.data);
        this.#socket.onopen = (e) => this.#completeHandshake();
    }

    #completeHandshake() {
        const message = JSON.stringify({
            "command": "handshake"
        });

        this.#socket.send(message);
    }

    #handleMessage(data) {
        this.#responseListeners.forEach(l => l(data));
    }

    send(input) {
        const message = JSON.stringify({
            "command": "input",
            "value": input
        });

        this.#socket.send(message);
    }

    addResponseListener(listener) {
        this.#responseListeners.push(listener);
    }
}