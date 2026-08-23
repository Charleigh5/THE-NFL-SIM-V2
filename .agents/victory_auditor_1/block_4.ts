export function playTackleImpact(audioCtx: AudioContext, kineticEnergyJoules: number): void {
  const now = audioCtx.currentTime;
  const normalizedEnergy = Math.min(1.0, Math.max(0.1, kineticEnergyJoules / 3500));
  
  // Layer 1: Sub-Bass Thud
  const thudOsc = audioCtx.createOscillator();
  const thudGain = audioCtx.createGain();
  thudOsc.type = "sine";
  thudOsc.frequency.setValueAtTime(140, now);
  thudOsc.frequency.exponentialRampToValueAtTime(28, now + 0.16);
  thudGain.gain.setValueAtTime(0.65 * normalizedEnergy, now);
  thudGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
  thudOsc.connect(thudGain);
  thudGain.connect(audioCtx.destination);
  thudOsc.start(now);
  thudOsc.stop(now + 0.2);
  
  // Layer 2: Pad Crack (Filtered Noise Burst)
  const bufferSize = audioCtx.sampleRate * 0.04;
  const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }
  const noiseSource = audioCtx.createBufferSource();
  noiseSource.buffer = noiseBuffer;
  
  const padFilter = audioCtx.createBiquadFilter();
  padFilter.type = "bandpass";
  padFilter.frequency.setValueAtTime(3200, now);
  padFilter.Q.setValueAtTime(2.2, now);
  
  const padGain = audioCtx.createGain();
  padGain.gain.setValueAtTime(0.85 * normalizedEnergy, now);
  padGain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
  
  noiseSource.connect(padFilter);
  padFilter.connect(padGain);
  padGain.connect(audioCtx.destination);
  noiseSource.start(now);
}