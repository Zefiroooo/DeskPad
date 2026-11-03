  // Switch
        const touchpad_switch = document.getElementById('touchpad-switch');
        const presenter_switch = document.getElementById('presenter-switch');
        const touchpad_mode = document.getElementById('touchpad-mode');
        const presenter_mode = document.getElementById('presenter-mode')

        // window.location.host otomatis membaca IP dan Port laptop tempat halaman web ini dibuka
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socket = new WebSocket(`${protocol}//${window.location.host}/ws`);

        // Touchpad
        const pad = document.getElementById('touchpad');

        // Click
        const left_button = document.getElementById('left-click');
        const right_button = document.getElementById('right-click');

        // Keys
        const prev = document.getElementById("prev-button");
        const next = document.getElementById("next-button");
        const start = document.getElementById("start-button");
        const exit = document.getElementById("exit-button");
        const blank = document.getElementById("blank-button");

        // Voice Controls
        const voice_button = document.getElementById("voice-button") || document.getElementById("voice");
        const voice_feedback = document.getElementById("voice-feedback");
        const voice_feedback_text = document.getElementById("voice-feedback-text");
        const voice_feedback_icon = document.getElementById("voice-feedback-icon");
        const voice_label = document.getElementById("voice-label");
        const voice_icon = document.getElementById("voice-icon");

        let isListening = false;
        let voiceTimer = null;

        function showVoiceStatus(text, icon = "🎙️", isError = false, duration = 3000) {
            if (!voice_feedback || !voice_feedback_text) return;
            if (voiceTimer) clearTimeout(voiceTimer);

            voice_feedback_text.textContent = text;
            if (voice_feedback_icon) voice_feedback_icon.textContent = icon;
            voice_feedback.classList.remove('hidden');

            if (isError) {
                voice_feedback.className = "px-3 py-1.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs font-medium text-center transition-all flex items-center justify-center gap-1.5 shadow-sm";
            } else {
                voice_feedback.className = "px-3 py-1.5 bg-indigo-50 border border-indigo-200 text-indigo-800 rounded-xl text-xs font-medium text-center transition-all flex items-center justify-center gap-1.5 shadow-sm";
            }

            if (duration > 0) {
                voiceTimer = setTimeout(() => {
                    if (!isListening) {
                        voice_feedback.classList.add('hidden');
                    }
                }, duration);
            }
        }

        function setListeningUI(listening) {
            isListening = listening;
            if (!voice_button) return;

            if (listening) {
                voice_button.classList.remove('bg-white', 'text-indigo-600', 'text-slate-700');
                voice_button.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
                if (voice_label) voice_label.textContent = "Mendengarkan...";
                if (voice_icon) voice_icon.textContent = "🔴";
                showVoiceStatus("Mendengarkan... Silakan bicara (Lanjut, Kembali, Mulai, Stop, dll)", "🎙️", false, 0);
            } else {
                voice_button.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
                voice_button.classList.add('bg-white', 'text-indigo-600');
                if (voice_label) voice_label.textContent = "Kontrol Suara";
                if (voice_icon) voice_icon.textContent = "🎙️";
            }
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'id-ID';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => {
                setListeningUI(true);
            };

            recognition.onresult = (event) => {
                if (!event.results || !event.results[0] || !event.results[0][0]) return;
                const transcript = event.results[0][0].transcript;
                console.log("Suara terdeteksi:", transcript);
                showVoiceStatus(`"${transcript}"`, "🗣️", false, 3000);

                if (socket.readyState === WebSocket.OPEN) {
                    socket.send(JSON.stringify({
                        type: "voice",
                        text: transcript
                    }));
                }
            };

            recognition.onerror = (event) => {
                console.warn("Speech recognition error:", event.error);
                let msg = "Gagal mengenali suara.";
                if (event.error === 'not-allowed') {
                    msg = "Izin mikrofon ditolak oleh browser.";
                } else if (event.error === 'no-speech') {
                    msg = "Tidak ada suara terdeteksi.";
                } else if (event.error === 'network') {
                    msg = "Masalah jaringan suara.";
                }
                showVoiceStatus(msg, "⚠️", true, 3000);
                setListeningUI(false);
            };

            recognition.onend = () => {
                setListeningUI(false);
            };
        } else {
            console.warn("Web Speech API tidak didukung pada browser ini.");
        }

        if (voice_button) {
            voice_button.addEventListener('click', () => {
                if (!recognition) {
                    alert("Web Speech API tidak didukung pada browser ini. Silakan gunakan browser Google Chrome.");
                    return;
                }

                if (isListening) {
                    try {
                        recognition.stop();
                    } catch (err) {
                        console.error(err);
                    }
                } else {
                    try {
                        recognition.start();
                    } catch (err) {
                        console.warn("Recognition start error:", err);
                    }
                }
            });
        }

        // Listener balasan WebSocket
        socket.addEventListener('message', (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === "voice_ack") {
                    const isUnknown = data.action === "unknown";
                    showVoiceStatus(data.message, isUnknown ? "❓" : "✅", isUnknown, 3000);
                }
            } catch (e) {
                console.error("Gagal memproses pesan socket:", e);
            }
        });



        // Function
        touchpad_switch.addEventListener('click', (e) =>{
            touchpad_switch.classList.remove('bg-slate-100');
            presenter_switch.classList.add('bg-slate-100');

            touchpad_mode.classList.remove('hidden');
            presenter_mode.classList.add('hidden');
        })

        presenter_switch.addEventListener('click', (e) =>{
            touchpad_switch.classList.add('bg-slate-100');
            presenter_switch.classList.remove('bg-slate-100');

            touchpad_mode.classList.add('hidden');
            presenter_mode.classList.remove('hidden');
        })



        let lastX = 0;
        let lastY = 0;

        pad.addEventListener('touchstart', (e) => {
            lastX = e.touches[0].clientX
            lastY = e.touches[0].clientY
        });

        pad.addEventListener('touchmove', (e) => {
            e.preventDefault()
            
            const currentX = e.touches[0].clientX
            const currentY = e.touches[0].clientY
            
            if (e.targetTouches.length === 1) {
    
                const dx = currentX - lastX
                const dy = currentY - lastY
    
                lastX = currentX
                lastY = currentY
    
                if (socket.readyState == WebSocket.OPEN) {
    
                    socket.send(JSON.stringify({
                        type: "move",
                        dx : Math.round(dx),
                        dy : Math.round(dy)
                    }));
                }
            } else if (e.targetTouches.length === 2) {
                const dy = currentY - lastY
                lastY = currentY

                if(socket.readyState == WebSocket.OPEN)
                socket.send(JSON.stringify({
                    type : "scroll",
                    dy : Math.round(dy)
            }))
            }
        })

        left_button.addEventListener('touchstart', (e) => {
            e.preventDefault()

            if(socket.readyState == WebSocket.OPEN)
                socket.send(JSON.stringify({
                type : "click",
                button : "left",
                action : "down"
            }))
        })

        const leftButtonRelease = (e) => {
            e.preventDefault()

            if(socket.readyState == WebSocket.OPEN)
                socket.send(JSON.stringify({
                type : "click",
                button : "left",
                action : "up"
            }))
        }

        left_button.addEventListener('touchend', leftButtonRelease)
        left_button.addEventListener('touchcancel', leftButtonRelease)


        right_button.addEventListener('touchstart', (e) => {
            e.preventDefault()

            if(socket.readyState == WebSocket.OPEN)
            socket.send(JSON.stringify({
                type : "click",
                button : "right",
                action : "down"
            }))
        })

        const rightButtonRelease = (e) => {
            e.preventDefault()

            if(socket.readyState == WebSocket.OPEN)
                socket.send(JSON.stringify({
                type : "click",
                button : "right",
                action : "up"
            }))
        }

        right_button.addEventListener('touchend', rightButtonRelease)
        right_button.addEventListener('touchcancel', rightButtonRelease)

        function sendKey(key_name) {
            if (socket.readyState == WebSocket.OPEN){
                socket.send(JSON.stringify({
                    type : "key",
                    key_name : key_name
                }))
            }
        }

        prev.addEventListener("click", () => sendKey("prev"));
        next.addEventListener("click", () => sendKey("next"));
        start.addEventListener("click", () => sendKey("start_canva"));
        exit.addEventListener("click", () => sendKey("exit"));
        blank.addEventListener("click", () => sendKey("black"))

