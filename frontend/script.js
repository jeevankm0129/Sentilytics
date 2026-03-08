document.addEventListener("DOMContentLoaded", () => {

    /* =========================================
       1. MORPHIC PARTICLE ENGINE (Background)
       ========================================= */
    const canvas = document.getElementById('particle-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particlesArray = [];
        let mouse = { x: null, y: null, radius: 150 };

        function setCanvasSize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        setCanvasSize();
        window.addEventListener('resize', () => {
            setCanvasSize();
            initParticles();
        });

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.x;
            mouse.y = e.y;
        });

        window.addEventListener('mouseout', () => {
            mouse.x = undefined;
            mouse.y = undefined;
        });

        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x;
                this.y = y;
                this.directionX = directionX;
                this.directionY = directionY;
                this.size = size;
                this.color = color;
                this.baseX = this.x;
                this.baseY = this.y;
                this.density = (Math.random() * 30) + 1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = this.color;
                ctx.fill();
            }

            update() {
                if (this.x > canvas.width || this.x < 0) this.directionX = -this.directionX;
                if (this.y > canvas.height || this.y < 0) this.directionY = -this.directionY;

                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < mouse.radius) {
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    let force = (mouse.radius - distance) / mouse.radius;
                    this.x -= forceDirectionX * force * this.density;
                    this.y -= forceDirectionY * force * this.density;
                } else {
                    if (this.x !== this.baseX) this.x -= (this.x - this.baseX) / 50;
                    if (this.y !== this.baseY) this.y -= (this.y - this.baseY) / 50;
                }

                this.x += this.directionX;
                this.y += this.directionY;
                this.draw();
            }
        }

        function initParticles() {
            particlesArray = [];
            let numberOfParticles = 400;

            for (let i = 0; i < numberOfParticles; i++) {
                let size = (Math.random() * 1.5) + 0.1;
                let x = Math.random() * innerWidth;
                let y = Math.random() * innerHeight;
                let directionX = (Math.random() * 0.4) - 0.2;
                let directionY = (Math.random() * 0.4) - 0.2;
                let color = 'rgb(222, 226, 255)' ; // Stellar Blue

                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }

        function connect() {
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let distance = ((particlesArray[a].x - particlesArray[b].x) ** 2) +
                        ((particlesArray[a].y - particlesArray[b].y) ** 2);
                    if (distance < (canvas.width / 7) * (canvas.height / 7)) {
                        let opacity = 1 - (distance / 25000);
                        ctx.strokeStyle = `rgba(222, 226, 255, ${opacity * 0.2})`; // Stardust lines
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, innerWidth, innerHeight);
            particlesArray.forEach(p => p.update());
            connect();
        }

        initParticles();
        animate();
    }

    /* =========================================
       2. SENTIMENT ANALYSIS LOGIC
       ========================================= */
    const analyzeBtn = document.getElementById('analyzeBtn');
    let sentimentChart = null;

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            const fileInput = document.getElementById('fileInput');
            const rawText = document.getElementById('rawText').value;
            const loader = document.getElementById('loader');
            const resultsSection = document.getElementById('resultsSection');

            // 1. Prepare Data
            const formData = new FormData();
            if (fileInput.files[0]) {
                formData.append('file', fileInput.files[0]);
            } else if (rawText.trim()) {
                formData.append('raw_text', rawText);
            } else {
                alert("Please upload a file or paste some text.");
                return;
            }

            // 2. UI Feedback
            loader.classList.remove('hidden');
            resultsSection.classList.add('hidden');
            document.querySelectorAll('.card').forEach(card => card.classList.remove('show'));

            try {
                // 3. API Call
                const response = await fetch('http://localhost:8000/analyze', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error('Analysis failed');
                const data = await response.json();

                // 4. Update UI
                document.getElementById('commentCount').textContent = data.number_of_comments_processed.toLocaleString();
                document.getElementById('summaryText').textContent = data.summary_text;
                document.getElementById('wordcloudImg').src = data.wordcloud_image;

                const kwList = document.getElementById('keywordList');
                kwList.innerHTML = data.top_keywords
                    .map(kw => `<li><span>${kw.word}</span><strong>${kw.count}</strong></li>`)
                    .join('');

                // 5. Render Chart
                renderChart(data.sentiment_distribution);

                // 6. Reveal with Staggered Animation
                loader.classList.add('hidden');
                resultsSection.classList.remove('hidden');

                resultsSection.querySelectorAll('.card').forEach((card, index) => {
                    setTimeout(() => card.classList.add('show'), index * 150);
                });

            } catch (error) {
                console.error(error);
                alert("Processing Error: Check if the backend server is running.");
                loader.classList.add('hidden');
            }
        });
    }

    function renderChart(distribution) {
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        if (sentimentChart) sentimentChart.destroy();

        sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(distribution),
                datasets: [{
                    data: Object.values(distribution),
                    backgroundColor: ['#495AEE', '#929BEC', '#1F027F'],
                    borderColor: 'rgba(220, 226, 244, 0.1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#DCE2F4', font: { family: 'Inter', size: 12 } }
                    }
                }
            }
        });
    }
});
