/**
 * Gridiron Sound Effects & Spatial Audio Engine
 * ==============================================
 * 100% offline synthesized Web Audio API sound designer for Madden / College Football 25 UI.
 * Zero external audio file download dependencies.
 *
 * Capabilities:
 * - 2D Field Spatial Panning (StereoPannerNode mapped to [0, 120] yardline coordinates)
 * - Kinetic Momentum Impact Synthesis (sub-bass thud + pad snap scaled by collision momentum)
 * - EPA-Driven Resonant Crowd Engine (positive EPA cheers vs negative EPA groans)
 * - Procedural Vocal Cadence Formant Synthesis ("Blue 80! Set, Hut!")
 * - Tactile UI clicks, whistle frequency modulation, and stadium brass horns
 */

export interface SpatialAudioConfig {
  volume: number; // [0.0, 1.0]
  isMuted: boolean;
  spatialAudioEnabled: boolean;
  crowdEnabled: boolean;
  sfxEnabled: boolean;
}

export interface HitIntensityProfile {
  gain: number;
  subFreq: number;
  snapFreq: number;
  duration: number;
}

export type CrowdReactionType = "ROAR" | "GROAN" | "MURMUR";
export type CadenceType = "hut" | "audible" | "set";

/**
 * Maps field Cartesian X coordinate [0, 120] (including endzones) to stereo pan [-0.85, 0.85]
 * Midfield (x = 60) maps to center (0.0).
 */
export function calculateSpatialPan(fieldX: number): number {
  const clampedX = Math.max(0, Math.min(120, fieldX));
  const rawPan = ((clampedX - 60) / 60) * 0.85;
  return Math.max(-0.85, Math.min(0.85, Number(rawPan.toFixed(3))));
}

/**
 * Calculates physical acoustic attributes for collisions based on kinetic momentum (kg * m/s).
 * Standard tackle: ~850 kg*m/s. Big hits: 1500 - 2500 kg*m/s.
 */
export function calculateHitIntensity(momentum: number, baseVolume: number = 0.5): HitIntensityProfile {
  const clampedMom = Math.max(200, Math.min(3000, momentum));
  const normalized = (clampedMom - 200) / 2800; // [0.0, 1.0]

  const gain = (0.15 + normalized * 0.8) * Math.max(0, Math.min(1, baseVolume));
  const subFreq = 160 - normalized * 65; // 160Hz down to deep 95Hz
  const snapFreq = 600 + normalized * 600; // 600Hz up to 1200Hz
  const duration = 0.12 + normalized * 0.16; // 0.12s to 0.28s

  return {
    gain: Number(gain.toFixed(3)),
    subFreq: Math.round(subFreq),
    snapFreq: Math.round(snapFreq),
    duration: Number(duration.toFixed(3)),
  };
}

/**
 * Classifies game momentum EPA deltas into procedural crowd acoustic profiles.
 */
export function classifyCrowdReaction(epaDelta: number): CrowdReactionType {
  if (epaDelta >= 1.5) return "ROAR";
  if (epaDelta <= -1.5) return "GROAN";
  return "MURMUR";
}

class GridironSoundEngine {
  private ctx: AudioContext | null = null;
  private isMuted: boolean = false;
  private volume: number = 0.5;
  private spatialAudioEnabled: boolean = true;
  private crowdEnabled: boolean = true;
  private sfxEnabled: boolean = true;

  constructor() {
    if (typeof window !== "undefined") {
      const savedMute = localStorage.getItem("gridiron_audio_muted");
      if (savedMute !== null) this.isMuted = savedMute === "true";

      const savedVol = localStorage.getItem("gridiron_audio_volume");
      if (savedVol !== null) this.volume = parseFloat(savedVol);

      const savedSpatial = localStorage.getItem("gridiron_audio_spatial");
      if (savedSpatial !== null) this.spatialAudioEnabled = savedSpatial === "true";

      const savedCrowd = localStorage.getItem("gridiron_audio_crowd");
      if (savedCrowd !== null) this.crowdEnabled = savedCrowd === "true";

      const savedSfx = localStorage.getItem("gridiron_audio_sfx");
      if (savedSfx !== null) this.sfxEnabled = savedSfx === "true";
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

  /**
   * Connects a gain node to destination directly or through StereoPannerNode if supported.
   */
  private connectWithPan(sourceNode: AudioNode, ctx: AudioContext, panValue: number = 0): AudioNode {
    if (this.spatialAudioEnabled && typeof ctx.createStereoPanner === "function") {
      try {
        const panner = ctx.createStereoPanner();
        panner.pan.setValueAtTime(Math.max(-1, Math.min(1, panValue)), ctx.currentTime);
        sourceNode.connect(panner);
        panner.connect(ctx.destination);
        return panner;
      } catch {
        sourceNode.connect(ctx.destination);
        return sourceNode;
      }
    }
    sourceNode.connect(ctx.destination);
    return sourceNode;
  }

  // --- Configuration Getters & Setters ---

  public setMuted(muted: boolean): void {
    this.isMuted = muted;
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_muted", String(muted));
    }
  }

  public getMuted(): boolean {
    return this.isMuted;
  }

  public setVolume(vol: number): void {
    this.volume = Math.max(0, Math.min(1, vol));
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_volume", String(this.volume));
    }
  }

  public getVolume(): number {
    return this.volume;
  }

  public setSpatialAudioEnabled(enabled: boolean): void {
    this.spatialAudioEnabled = enabled;
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_spatial", String(enabled));
    }
  }

  public getSpatialAudioEnabled(): boolean {
    return this.spatialAudioEnabled;
  }

  public setCrowdEnabled(enabled: boolean): void {
    this.crowdEnabled = enabled;
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_crowd", String(enabled));
    }
  }

  public getCrowdEnabled(): boolean {
    return this.crowdEnabled;
  }

  public setSfxEnabled(enabled: boolean): void {
    this.sfxEnabled = enabled;
    if (typeof window !== "undefined") {
      localStorage.setItem("gridiron_audio_sfx", String(enabled));
    }
  }

  public getSfxEnabled(): boolean {
    return this.sfxEnabled;
  }

  public getConfig(): SpatialAudioConfig {
    return {
      volume: this.volume,
      isMuted: this.isMuted,
      spatialAudioEnabled: this.spatialAudioEnabled,
      crowdEnabled: this.crowdEnabled,
      sfxEnabled: this.sfxEnabled,
    };
  }

  // --- Procedural Acoustic Synthesizers ---

  /**
   * Play spatial collision hit with sub-bass thud and transient pad clack.
   * Field coordinates: fieldX in yards [0, 120].
   */
  public playSpatialHit(fieldX: number = 60, _fieldY: number = 26.65, momentum: number = 850): void {
    if (this.isMuted || !this.sfxEnabled) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const pan = calculateSpatialPan(fieldX);
      const profile = calculateHitIntensity(momentum, this.volume);

      // 1. Sub-bass boom oscillator
      const subOsc = ctx.createOscillator();
      const subGain = ctx.createGain();
      subOsc.type = "triangle";
      subOsc.frequency.setValueAtTime(profile.subFreq, now);
      subOsc.frequency.exponentialRampToValueAtTime(28, now + profile.duration);

      subGain.gain.setValueAtTime(profile.gain, now);
      subGain.gain.exponentialRampToValueAtTime(0.001, now + profile.duration);

      subOsc.connect(subGain);
      this.connectWithPan(subGain, ctx, pan);

      // 2. High transient snap (pad plastic impact)
      const snapOsc = ctx.createOscillator();
      const snapGain = ctx.createGain();
      snapOsc.type = "sawtooth";
      snapOsc.frequency.setValueAtTime(profile.snapFreq, now);
      snapOsc.frequency.exponentialRampToValueAtTime(80, now + 0.04);

      snapGain.gain.setValueAtTime(profile.gain * 0.45, now);
      snapGain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

      snapOsc.connect(snapGain);
      this.connectWithPan(snapGain, ctx, pan);

      subOsc.start(now);
      snapOsc.start(now);
      subOsc.stop(now + profile.duration);
      snapOsc.stop(now + 0.04);
    } catch {
      // Safe fallback
    }
  }

  /**
   * Play referee whistle (twin tone with trill modulation and optional spatial pan).
   */
  public playSpatialWhistle(fieldX?: number): void {
    if (this.isMuted || !this.sfxEnabled) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const pan = fieldX !== undefined ? calculateSpatialPan(fieldX) : 0;

      const osc1 = ctx.createOscillator();
      const osc2 = ctx.createOscillator();
      const gain = ctx.createGain();

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

      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.35 * this.volume, now + 0.04);
      gain.gain.setValueAtTime(0.35 * this.volume, now + 0.28);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

      osc1.connect(gain);
      osc2.connect(gain);
      this.connectWithPan(gain, ctx, pan);

      lfo.start(now);
      osc1.start(now);
      osc2.start(now);

      lfo.stop(now + 0.45);
      osc1.stop(now + 0.45);
      osc2.stop(now + 0.45);
    } catch {
      // Safe fallback
    }
  }

  /**
   * Procedural Quarterback Cadence Formant Synthesis ("Blue 80! Set, Hut!")
   */
  public playCadence(type: CadenceType = "hut"): void {
    if (this.isMuted || !this.sfxEnabled) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;

      if (type === "hut") {
        // Sharp acoustic snap punch (320Hz + 740Hz formant pair)
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gain = ctx.createGain();

        osc1.type = "triangle";
        osc1.frequency.setValueAtTime(320, now);
        osc1.frequency.exponentialRampToValueAtTime(140, now + 0.09);

        osc2.type = "sine";
        osc2.frequency.setValueAtTime(740, now);
        osc2.frequency.exponentialRampToValueAtTime(220, now + 0.09);

        gain.gain.setValueAtTime(0.38 * this.volume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);

        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + 0.09);
        osc2.stop(now + 0.09);
      } else if (type === "audible") {
        // Two-tone audible alert chirp (880Hz -> 1100Hz)
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.setValueAtTime(1100, now + 0.05);

        gain.gain.setValueAtTime(0.25 * this.volume, now);
        gain.gain.setValueAtTime(0.25 * this.volume, now + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now);
        osc.stop(now + 0.14);
      } else {
        // "set" steady vocal formant
        const osc = ctx.createOscillator();
        const filter = ctx.createBiquadFilter();
        const gain = ctx.createGain();

        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(220, now);

        filter.type = "bandpass";
        filter.frequency.setValueAtTime(550, now);
        filter.Q.setValueAtTime(3.0, now);

        gain.gain.setValueAtTime(0.28 * this.volume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now);
        osc.stop(now + 0.12);
      }
    } catch {
      // Safe fallback
    }
  }

  /**
   * EPA-Driven Resonant Crowd Engine.
   * Generates dynamic pink-noise acoustic swells responding to big plays or turnovers.
   */
  public updateCrowdIntensity(epaDelta: number, _homeWinProb: number = 0.5): void {
    if (this.isMuted || !this.crowdEnabled) return;
    const ctx = this.initCtx();
    if (!ctx) return;

    try {
      const now = ctx.currentTime;
      const reaction = classifyCrowdReaction(epaDelta);
      const bufferSize = Math.floor(ctx.sampleRate * (reaction === "ROAR" ? 1.6 : 1.2));
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);

      // Pinkish noise generator
      let b0 = 0, b1 = 0, b2 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.969 * b2 + white * 0.153852;
        data[i] = (b0 + b1 + b2) * 0.16;
      }

      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();

      if (reaction === "ROAR") {
        // Resonant upward frequency sweep
        filter.type = "bandpass";
        filter.frequency.setValueAtTime(450, now);
        filter.frequency.linearRampToValueAtTime(900, now + 0.5);
        filter.Q.setValueAtTime(1.5, now);

        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.38 * this.volume, now + 0.35);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.6);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        noise.start(now);
        noise.stop(now + 1.6);
      } else if (reaction === "GROAN") {
        // Descending muffled groan
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(480, now);
        filter.frequency.linearRampToValueAtTime(180, now + 0.8);
        filter.Q.setValueAtTime(2.0, now);

        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.28 * this.volume, now + 0.25);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        noise.start(now);
        noise.stop(now + 1.2);
      } else {
        // Ambient murmuring swell
        filter.type = "bandpass";
        filter.frequency.setValueAtTime(360, now);
        filter.Q.setValueAtTime(1.0, now);

        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.18 * this.volume, now + 0.2);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);

        noise.start(now);
        noise.stop(now + 0.8);
      }
    } catch {
      // Safe fallback
    }
  }

  // --- Legacy Backward Compatible API Methods ---

  public playWhistle(): void {
    this.playSpatialWhistle();
  }

  public playStadiumHorn(): void {
    if (this.isMuted || !this.sfxEnabled) return;
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

  public playSnap(): void {
    if (this.isMuted || !this.sfxEnabled) return;
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

  public playHit(): void {
    this.playSpatialHit(60, 26.65, 850);
  }

  public playCrowdRoar(): void {
    this.updateCrowdIntensity(3.0, 0.7);
  }
}

export const soundEffects = new GridironSoundEngine();
