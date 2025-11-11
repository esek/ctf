const wsUri = `ws://${window.location.host}/envs/browser_devtools/`;
console.log(wsUri);
const websocket = new WebSocket(wsUri);