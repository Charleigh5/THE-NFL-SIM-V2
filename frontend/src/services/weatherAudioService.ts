/**
 * Procedural Weather Audio Synthesizer
 * 100% offline Web Audio API synthesis for rain, thunder, and blizzard winds.
 * Zero external audio files required.
 */

class WeatherAudioEngine {
  private ctx: AudioContext | null = null;
  private rainNode: AudioNode | null = null;
  private rainGain: GainNode | null = null;
  private windNode: AudioNode | null = null;
  private windGain: GainNode | null = null;
  private masterGain: GainNode | null = null;
  private isInitialized = false;

  private initAudio() {
    if (this.isInitialized && this.ctx) return;
    try {
      const AudioCtx =
        window.AudioContext ||
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new AudioCtx();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0.5, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);
      this.isInitialized = true;
    } catch {
      // Audio context creation suppressed if not allowed yet
    }
  }

  public setMasterVolume(vol: number) {
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setTargetAtTime(
        Math.max(0, Math.min(1, vol)),
        this.ctx.currentTime,
        0.05
      );
    }
  }

  /**
   * Start procedural rain sound
   */
  public startRain(density = 0.8) {
    this.initAudio();
    if (!this.ctx || !this.masterGain) return;
    if (this.rainNode) return; // already active

    const bufferSize = this.ctx.sampleRate * 2;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);

    // Generate pink noise for soft rain hiss
    let b0 = 0,
      b1 = 0,
      b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.969 * b2 + white * 0.153852;
      output[i] = (b0 + b1 + b2) * 0.15;
    }

    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    // Filter to sound like rain on turf and metal stadium roofs
    const filter = this.ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.setValueAtTime(1200 + density * 800, this.ctx.currentTime);

    this.rainGain = this.ctx.createGain();
    this.rainGain.gain.setValueAtTime(density * 0.35, this.ctx.currentTime);

    whiteNoise.connect(filter);
    filter.connect(this.rainGain);
    this.rainGain.connect(this.masterGain);

    whiteNoise.start();
    this.rainNode = whiteNoise;
  }

  public stopRain() {
    if (this.rainNode && this.ctx) {
      try {
        (this.rainNode as AudioScheduledSourceNode).stop();
      } catch {
        // Ignored
      }
      this.rainNode.disconnect();
      this.rainNode = null;
    }
  }

  /**
   * Start procedural blizzard wind whoosh
   */
  public startWind(speedMph = 20) {
    this.initAudio();
    if (!this.ctx || !this.masterGain) return;
    if (this.windNode) return;

    const bufferSize = this.ctx.sampleRate * 3;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);

    // Brown noise for deep wind howl
    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      output[i] = (lastOut + 0.02 * white) / 1.02;
      lastOut = output[i];
      output[i] *= 3.5;
    }

    const brownNoise = this.ctx.createBufferSource();
    brownNoise.buffer = noiseBuffer;
    brownNoise.loop = true;

    const bandpass = this.ctx.createBiquadFilter();
    bandpass.type = "bandpass";
    bandpass.frequency.setValueAtTime(260, this.ctx.currentTime);
    bandpass.Q.setValueAtTime(2.5, this.ctx.currentTime);

    this.windGain = this.ctx.createGain();
    const gainVal = Math.min(0.4, (speedMph / 50) * 0.35);
    this.windGain.gain.setValueAtTime(gainVal, this.ctx.currentTime);

    brownNoise.connect(bandpass);
    bandpass.connect(this.windGain);
    this.windGain.connect(this.masterGain);

    brownNoise.start();
    this.windNode = brownNoise;
  }

  public stopWind() {
    if (this.windNode && this.ctx) {
      try {
        (this.windNode as AudioScheduledSourceNode).stop();
      } catch {
        // Ignored
      }
      this.windNode.disconnect();
      this.windNode = null;
    }
  }

  /**
   * Synthesize a realistic rolling thunder strike
   */
  public playThunderStrike(intensity = 1.0) {
    this.initAudio();
    if (!this.ctx || !this.masterGain) return;
    const t = this.ctx.currentTime;

    // Sub-bass crack oscillator
    const osc = this.ctx.createOscillator();
    osc.type = "triangle";
    osc.frequency.setValueAtTime(90, t);
    osc.frequency.exponentialRampToValueAtTime(32, t + 0.8);

    const oscGain = this.ctx.createGain();
    oscGain.gain.setValueAtTime(intensity * 0.8, t);
    oscGain.gain.exponentialRampToValueAtTime(0.001, t + 1.2);

    osc.connect(oscGain);
    oscGain.connect(this.masterGain);

    osc.start(t);
    osc.stop(t + 1.2);

    // Deep rolling thunder noise tail
    const bufferSize = this.ctx.sampleRate * 2.5;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = (Math.random() * 2 - 1) * Math.exp(-i / (this.ctx.sampleRate * 0.9));
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = noiseBuffer;

    const lp = this.ctx.createBiquadFilter();
    lp.type = "lowpass";
    lp.frequency.setValueAtTime(180, t);
    lp.frequency.linearRampToValueAtTime(80, t + 2.0);

    const rumbleGain = this.ctx.createGain();
    rumbleGain.gain.setValueAtTime(intensity * 0.6, t);
    rumbleGain.gain.exponentialRampToValueAtTime(0.001, t + 2.5);

    noise.connect(lp);
    lp.connect(rumbleGain);
    rumbleGain.connect(this.masterGain);

    noise.start(t);
    noise.stop(t + 2.5);
  }

  public stopAll() {
    this.stopRain();
    this.stopWind();
  }
}

export const weatherAudio = new WeatherAudioEngine();
