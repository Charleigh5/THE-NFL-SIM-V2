/**
 * Gridiron Sound Effects Engine
 * ==============================
 * 100% offline synthesized Web Audio API sound designer for Madden / College Football 25 UI.
 * Zero external audio file download dependencies.
 */

class GridironSoundEngine {
  private ctx: AudioContext | null = null;
  private isMuted: boolean = false;
  private volume: number = 0.5;

  constructor() {
    if (typeof window !== "undefined") {
      const savedMute = localStorage.getItem("gridiron_audio_muted");
      this.isMuted = savedMute === "true";
      const savedVol = localStorage.getItem("gridiron_audio_volume");
      if (savedVol) this.volume = parseFloat(savedVol);
    }
  }

  private initCtx(): AudioContext | null {
    if (typeof window === "undefined") return null;
    if (!this.ctx) {
      const AudioCtxClass =
        window.AudioContext ||
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioCtxClass) {
        this.ctx = new AudioCtxClass();
      }
    }
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume().catch(() => {});
    }
    return this.ctx;
  }

  public setMuted(muted: boolean) {
    this.isMuted = muted;
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_muted", String(muted));
    }
  }

  public getMuted(): boolean {
    return this.isMuted;
  }

  public setVolume(vol: number) {
    this.volume = Math.max(0, Math.min(1, vol));
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_volume", String(this.volume));
    }
  }

  /**
   * Play referee whistle (frequency-modulated twin tone with trill)
   */
  public playWhistle() {
    if (this.isMuted) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const osc1 = ctx.createOscillator();
      const osc2 = ctx.createOscillator();
      const gain = ctx.createGain();

      // Twin whistle resonant frequencies
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(2600, now);
      osc2.type = "sine";
      osc2.frequency.setValueAtTime(2900, now);

      // Trill modulation (shaking air vibration)
      const lfo = ctx.createOscillator();
      const lfoGain = ctx.createGain();
      lfo.frequency.setValueAtTime(28, now);
      lfoGain.gain.setValueAtTime(140, now);
      lfo.connect(osc1.frequency);
      lfo.connect(osc2.frequency);

      // Envelope
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.35 * this.volume, now + 0.04);
      gain.gain.setValueAtTime(0.35 * this.volume, now + 0.28);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(ctx.destination);

      lfo.start(now);
      osc1.start(now);
      osc2.start(now);

      lfo.stop(now + 0.45);
      osc1.stop(now + 0.45);
      osc2.stop(now + 0.45);
    } catch {
      // Ignore browser autoplay restrictions gracefully
    }
  }

  /**
   * Play stadium quarter / game end horn (deep brassy power blast)
   */
  public playStadiumHorn() {
    if (this.isMuted) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const sub = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();

      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(130, now + 0.6);

      sub.type = "sine";
      sub.frequency.setValueAtTime(70, now);

      filter.type = "lowpass";
      filter.frequency.setValueAtTime(800, now);
      filter.Q.setValueAtTime(3, now);

      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.4 * this.volume, now + 0.05);
      gain.gain.setValueAtTime(0.35 * this.volume, now + 0.5);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

      osc.connect(filter);
      sub.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      sub.start(now);
      osc.stop(now + 0.8);
      sub.stop(now + 0.8);
    } catch {
      // Safe fallback
    }
  }

  /**
   * Play tactile UI snap / card selection click
   */
  public playSnap() {
    if (this.isMuted) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(850, now);
      osc.frequency.exponentialRampToValueAtTime(180, now + 0.04);

      gain.gain.setValueAtTime(0.2 * this.volume, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 0.04);
    } catch {
      // Safe fallback
    }
  }

  /**
   * Play heavy tackle impact sound
   */
  public playHit() {
    if (this.isMuted) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;

      // Sub thud
      const osc = ctx.createOscillator();
      const oscGain = ctx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(120, now);
      osc.frequency.exponentialRampToValueAtTime(30, now + 0.18);

      oscGain.gain.setValueAtTime(0.45 * this.volume, now);
      oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);

      osc.connect(oscGain);
      oscGain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.18);
    } catch {
      // Safe fallback
    }
  }

  /**
   * Play crowd roar swell
   */
  public playCrowdRoar() {
    if (this.isMuted) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const bufferSize = ctx.sampleRate * 1.5;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);

      // Pinkish noise generator
      let b0 = 0,
        b1 = 0,
        b2 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.969 * b2 + white * 0.153852;
        data[i] = (b0 + b1 + b2) * 0.15;
      }

      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = "bandpass";
      filter.frequency.setValueAtTime(450, now);
      filter.Q.setValueAtTime(1.2, now);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(0.25 * this.volume, now + 0.4);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.4);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      noise.start(now);
      noise.stop(now + 1.4);
    } catch {
      // Safe fallback
    }
  }
}

export const soundEffects = new GridironSoundEngine();
