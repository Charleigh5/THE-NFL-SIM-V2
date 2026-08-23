export function playRefereeWhistle(audioCtx: AudioContext, intensity: number = 1.0): void {
  const now = audioCtx.currentTime;
  
  const osc1 = audioCtx.createOscillator();
  const osc2 = audioCtx.createOscillator();
  const lfo = audioCtx.createOscillator();
  const lfoGain = audioCtx.createGain();
  const masterGain = audioCtx.createGain();
  
  // Dual fundamental frequencies creating acoustic beat interference
  osc1.type = "sine";
  osc1.frequency.setValueAtTime(2780, now);
  osc2.type = "sine";
  osc2.frequency.setValueAtTime(3090, now);
  
  // 28.5 Hz Pea Rattle Modulation
  lfo.type = "sine";
  lfo.frequency.setValueAtTime(28.5, now);
  lfoGain.gain.setValueAtTime(160, now);
  lfo.connect(osc1.frequency);
  lfo.connect(osc2.frequency);
  
  // ADSR Gain Envelope
  const peakGain = 0.38 * Math.min(1.0, Math.max(0.1, intensity));
  masterGain.gain.setValueAtTime(0.0001, now);
  masterGain.gain.linearRampToValueAtTime(peakGain, now + 0.035);
  masterGain.gain.setValueAtTime(peakGain, now + 0.28);
  masterGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.48);
  
  osc1.connect(masterGain);
  osc2.connect(masterGain);
  masterGain.connect(audioCtx.destination);
  
  lfo.start(now);
  osc1.start(now);
  osc2.start(now);
  
  lfo.stop(now + 0.5);
  osc1.stop(now + 0.5);
  osc2.stop(now + 0.5);
}