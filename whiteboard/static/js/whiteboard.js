class Whiteboard {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.drawing = false;
        this.color = '#000000';
        this.lineWidth = 3;
        this.socket = new WebSocket(`wss://${window.location.host}/ws/whiteboard/${whiteboardId}/`);
        
        this.setupEventListeners();
        this.setupWebSocket();
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
        this.canvas.addEventListener('mousemove', this.draw.bind(this));
        this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
        this.canvas.addEventListener('mouseout', this.stopDrawing.bind(this));
        
        document.getElementById('color-picker').addEventListener('change', (e) => {
            this.color = e.target.value;
        });
        
        document.getElementById('brush-size').addEventListener('change', (e) => {
            this.lineWidth = e.target.value;
        });
    }
    
    setupWebSocket() {
        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type === 'draw') {
                this.drawFromData(data);
            } else if (data.type === 'clear') {
                this.clearCanvas();
            }
        };
    }
    
    startDrawing(e) {
        this.drawing = true;
        this.draw(e);
    }
    
    draw(e) {
        if (!this.drawing) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        this.ctx.lineWidth = this.lineWidth;
        this.ctx.lineCap = 'round';
        this.ctx.strokeStyle = this.color;
        this.ctx.lineTo(x, y);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        
        // Send drawing data to server
        this.socket.send(JSON.stringify({
            type: 'draw',
            x,
            y,
            color: this.color,
            lineWidth: this.lineWidth
        }));
    }
    
    stopDrawing() {
        this.drawing = false;
        this.ctx.beginPath();
    }
    
    drawFromData(data) {
        this.ctx.lineWidth = data.lineWidth;
        this.ctx.strokeStyle = data.color;
        this.ctx.lineTo(data.x, data.y);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(data.x, data.y);
    }
    
    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    clear() {
        this.clearCanvas();
        this.socket.send(JSON.stringify({
            type: 'clear'
        }));
    }
}

// Initialize whiteboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const whiteboard = new Whiteboard('whiteboard-canvas');
    window.whiteboard = whiteboard;
});