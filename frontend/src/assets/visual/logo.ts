/**
 * Procedural Logo Generator for NFL Simulation
 * Generates unique, non-trademarked abstract geometric logos
 * Uses deterministic hashing for consistent team branding
 */

import type { VisualTeam } from '../../types/broadcast';

// ============================================================================
// Type Definitions
// ============================================================================

export interface LogoConfig {
  teamId: string;
  city: string;
  name: string;
  primaryColor: string;
  secondaryColor: string;
  seed: number;
}

export interface ShapeDef {
  type: 'hexagon' | 'circle' | 'diamond' | 'shield' | 'abstract' | 'star' | 'triangle';
  sides?: number;
  rotation: number;
  scale: number;
  fillPattern: 'solid' | 'gradient' | 'stripes' | 'dots' | 'chevron';
}

export interface GeneratedLogo {
  svg: string;
  config: LogoConfig;
  shapes: ShapeDef[];
  hashCode: number;
  uniqueness: number; // 0-1 score against known patterns
}

// ============================================================================
// Deterministic Hash Functions
// ============================================================================

/**
 * DJB2 hash algorithm for deterministic seeding
 * Same input always produces same output
 */
function djb2Hash(str: string): number {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

/**
 * Seeded pseudo-random number generator (Mulberry32)
 * Produces repeatable random sequence from seed
 */
class SeededRandom {
  private seed: number;

  constructor(seed: number) {
    this.seed = seed;
  }

  next(): number {
    let t = (this.seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  nextInt(min: number, max: number): number {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }

  pick<T>(array: T[]): T {
    return array[this.nextInt(0, array.length - 1)];
  }
}

// ============================================================================
// Shape Generators
// ============================================================================

const SHAPE_TYPES: ShapeDef['type'][] = ['hexagon', 'circle', 'diamond', 'shield', 'abstract', 'star', 'triangle'];
const FILL_PATTERNS: ShapeDef['fillPattern'][] = ['solid', 'gradient', 'stripes', 'dots', 'chevron'];

function generateShape(rng: SeededRandom, _index: number): ShapeDef {
  const type = rng.pick(SHAPE_TYPES);
  const sides = type === 'hexagon' ? 6 : type === 'triangle' ? 3 : undefined;
  
  return {
    type,
    sides,
    rotation: rng.nextInt(0, 360),
    scale: 0.3 + rng.next() * 0.5, // 0.3 to 0.8
    fillPattern: rng.pick(FILL_PATTERNS),
  };
}

function renderShape(shape: ShapeDef, cx: number, cy: number, size: number, colors: string[]): string {
  const { type, rotation, scale, fillPattern } = shape;
  const scaledSize = size * scale;
  
  let path = '';
  
  switch (type) {
    case 'hexagon':
      path = createPolygon(cx, cy, scaledSize, 6, rotation);
      break;
    case 'circle':
      path = `<circle cx="${cx}" cy="${cy}" r="${scaledSize}" />`;
      break;
    case 'diamond':
      path = createPolygon(cx, cy, scaledSize, 4, rotation + 45);
      break;
    case 'shield':
      path = createShield(cx, cy, scaledSize, rotation);
      break;
    case 'abstract':
      path = createAbstract(cx, cy, scaledSize, rngForGlobal, rotation);
      break;
    case 'star':
      path = createStar(cx, cy, scaledSize, 5, rotation);
      break;
    case 'triangle':
      path = createPolygon(cx, cy, scaledSize, 3, rotation);
      break;
  }
  
  const gradientId = `grad-${Math.round(cx)}-${Math.round(cy)}`;
  const fill = fillPattern === 'gradient' 
    ? `url(#${gradientId})`
    : fillPattern === 'stripes'
    ? `url(#stripes-${Math.round(cx)})`
    : fillPattern === 'dots'
    ? `url(#dots-${Math.round(cy)})`
    : colors[0];
  
  let defs = '';
  if (fillPattern === 'gradient') {
    defs = `
      <defs>
        <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:${colors[0]};stop-opacity:1" />
          <stop offset="100%" style="stop-color:${colors[1]};stop-opacity:1" />
        </linearGradient>
      </defs>`;
  } else if (fillPattern === 'stripes') {
    defs = `
      <defs>
        <pattern id="stripes-${Math.round(cx)}" patternUnits="userSpaceOnUse" width="10" height="10">
          <rect width="10" height="10" fill="${colors[0]}" />
          <line x1="0" y1="0" x2="10" y2="10" stroke="${colors[1]}" strokeWidth="2" />
          <line x1="0" y1="10" x2="10" y2="0" stroke="${colors[1]}" strokeWidth="2" />
        </pattern>
      </defs>`;
  } else if (fillPattern === 'dots') {
    defs = `
      <defs>
        <pattern id="dots-${Math.round(cy)}" patternUnits="userSpaceOnUse" width="10" height="10">
          <rect width="10" height="10" fill="${colors[0]}" />
          <circle cx="5" cy="5" r="2" fill="${colors[1]}" />
        </pattern>
      </defs>`;
  }
  
  return `${defs}<path d="${path}" fill="${fill}" opacity="0.85" />`;
}

function createPolygon(cx: number, cy: number, radius: number, sides: number, rotation: number): string {
  const points: string[] = [];
  const angleStep = (2 * Math.PI) / sides;
  const rotationRad = (rotation * Math.PI) / 180;
  
  for (let i = 0; i < sides; i++) {
    const angle = i * angleStep + rotationRad;
    const x = cx + radius * Math.cos(angle);
    const y = cy + radius * Math.sin(angle);
    points.push(`${x.toFixed(2)},${y.toFixed(2)}`);
  }
  
  return `M ${points.join(' L ')} Z`;
}

function createShield(cx: number, cy: number, size: number, rotation: number): string {
  const rad = (rotation * Math.PI) / 180;
  const rotate = (x: number, y: number) => ({
    x: cx + (x - cx) * Math.cos(rad) - (y - cy) * Math.sin(rad),
    y: cy + (x - cx) * Math.sin(rad) + (y - cy) * Math.cos(rad),
  });
  
  const top = rotate(cx, cy - size);
  const leftMid = rotate(cx - size * 0.8, cy);
  const bottom = rotate(cx, cy + size * 1.2);
  const rightMid = rotate(cx + size * 0.8, cy);
  
  return `M ${top.x.toFixed(2)},${top.y.toFixed(2)} 
          Q ${leftMid.x.toFixed(2)},${leftMid.y.toFixed(2)} ${bottom.x.toFixed(2)},${bottom.y.toFixed(2)}
          Q ${rightMid.x.toFixed(2)},${rightMid.y.toFixed(2)} ${top.x.toFixed(2)},${top.y.toFixed(2)} Z`;
}

function createStar(cx: number, cy: number, outerRadius: number, points: number, rotation: number): string {
  const innerRadius = outerRadius * 0.4;
  const step = Math.PI / points;
  const rotationRad = (rotation * Math.PI) / 180 - Math.PI / 2;
  
  let path = '';
  for (let i = 0; i < points * 2; i++) {
    const radius = i % 2 === 0 ? outerRadius : innerRadius;
    const angle = i * step + rotationRad;
    const x = cx + radius * Math.cos(angle);
    const y = cy + radius * Math.sin(angle);
    path += (i === 0 ? 'M ' : 'L ') + `${x.toFixed(2)},${y.toFixed(2)}`;
  }
  
  return path + ' Z';
}

function createAbstract(cx: number, cy: number, size: number, _rng: SeededRandom, rotation: number): string {
  // Bezier curve-based abstract shape
  const rad = (rotation * Math.PI) / 180;
  const rotate = (x: number, y: number) => ({
    x: cx + (x - cx) * Math.cos(rad) - (y - cy) * Math.sin(rad),
    y: cy + (x - cx) * Math.sin(rad) + (y - cy) * Math.cos(rad),
  });
  
  const p1 = rotate(cx - size * 0.5, cy - size * 0.3);
  const c1 = rotate(cx - size * 0.8, cy + size * 0.2);
  const c2 = rotate(cx - size * 0.3, cy + size * 0.8);
  const p2 = rotate(cx + size * 0.4, cy + size * 0.6);
  const c3 = rotate(cx + size * 0.9, cy + size * 0.1);
  const c4 = rotate(cx + size * 0.6, cy - size * 0.5);
  
  return `M ${p1.x.toFixed(2)},${p1.y.toFixed(2)} 
          C ${c1.x.toFixed(2)},${c1.y.toFixed(2)} ${c2.x.toFixed(2)},${c2.y.toFixed(2)} ${p2.x.toFixed(2)},${p2.y.toFixed(2)}
          C ${c3.x.toFixed(2)},${c3.y.toFixed(2)} ${c4.x.toFixed(2)},${c4.y.toFixed(2)} ${p1.x.toFixed(2)},${p1.y.toFixed(2)} Z`;
}

// Global RNG instance for shape generation
let rngForGlobal: SeededRandom;

// ============================================================================
// Main Generator Class
// ============================================================================

export class ProceduralLogoGenerator {
  private cache: Map<string, GeneratedLogo> = new Map();

  /**
   * Generate a logo for a team
   * Deterministic: same team always produces same logo
   */
  generate(team: VisualTeam): GeneratedLogo {
    const cacheKey = `${team.id}-${team.city}-${team.name}`;
    const cached = this.cache.get(cacheKey);
    if (cached) return cached;

    const config: LogoConfig = {
      teamId: String(team.id),
      city: team.city || 'Unknown',
      name: team.name || 'Team',
      primaryColor: team.primary_color || '#003366',
      secondaryColor: team.secondary_color || '#FF6600',
      seed: djb2Hash(`${team.city}${team.name}${team.abbreviation}`),
    };

    rngForGlobal = new SeededRandom(config.seed);
    
    // Generate 2-4 layered shapes
    const numShapes = rngForGlobal.nextInt(2, 4);
    const shapes: ShapeDef[] = [];
    for (let i = 0; i < numShapes; i++) {
      shapes.push(generateShape(rngForGlobal, i));
    }

    // Render SVG
    const size = 200;
    const centerX = size / 2;
    const centerY = size / 2;
    const baseRadius = size * 0.4;
    
    let shapesSvg = '';
    shapes.forEach((shape, idx) => {
      const offset = idx * 15;
      shapesSvg += renderShape(
        shape,
        centerX + (idx % 2 === 0 ? offset : -offset),
        centerY + (idx % 3 === 0 ? offset * 0.5 : -offset * 0.5),
        baseRadius * (1 - idx * 0.15),
        [config.primaryColor, config.secondaryColor]
      );
    });

    // Add team abbreviation as text
    const abbrev = team.abbreviation || team.name.substring(0, 3).toUpperCase();
    const textElement = `
      <text x="${centerX}" y="${centerY + 10}" 
            font-family="Arial, sans-serif" 
            font-size="48" 
            font-weight="bold"
            fill="${this.getContrastingTextColor(config.primaryColor)}"
            text-anchor="middle"
            stroke="${config.secondaryColor}"
            stroke-width="2">
        ${abbrev}
      </text>`;

    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">
        <rect width="${size}" height="${size}" fill="transparent" />
        ${shapesSvg}
        ${textElement}
      </svg>`.trim();

    const result: GeneratedLogo = {
      svg,
      config,
      shapes,
      hashCode: config.seed,
      uniqueness: this.calculateUniqueness(shapes, config.seed),
    };

    this.cache.set(cacheKey, result);
    return result;
  }

  /**
   * Get contrasting text color (black or white)
   */
  private getContrastingTextColor(hexColor: string): string {
    const r = parseInt(hexColor.slice(1, 3), 16);
    const g = parseInt(hexColor.slice(3, 5), 16);
    const b = parseInt(hexColor.slice(5, 7), 16);
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return luminance > 0.5 ? '#000000' : '#FFFFFF';
  }

  /**
   * Calculate uniqueness score (0-1) based on shape diversity
   * Higher is better (more distinct from common patterns)
   */
  private calculateUniqueness(shapes: ShapeDef[], seed: number): number {
    const typeDiversity = new Set(shapes.map(s => s.type)).size / shapes.length;
    const patternDiversity = new Set(shapes.map(s => s.fillPattern)).size / shapes.length;
    const rotationVariance = shapes.reduce((acc, s, i) => {
      if (i === 0) return acc;
      return acc + Math.abs(s.rotation - shapes[i - 1].rotation);
    }, 0) / (shapes.length * 360);
    
    return Math.min(1, (typeDiversity + patternDiversity + rotationVariance) / 3 + seed % 100 / 1000);
  }

  /**
   * Export logo as PNG data URL (for canvas rendering)
   */
  async toPng(logo: GeneratedLogo, scale: number = 2): Promise<string> {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const size = 200 * scale;
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d')!;
        ctx.drawImage(img, 0, 0, size, size);
        resolve(canvas.toDataURL('image/png'));
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(logo.svg);
    });
  }

  /**
   * Clear cache (useful for testing or memory management)
   */
  clearCache(): void {
    this.cache.clear();
  }
}

// Singleton instance
const logoGenerator = new ProceduralLogoGenerator();

export function getLogoGenerator(): ProceduralLogoGenerator {
  return logoGenerator;
}

/**
 * Convenience function for quick logo generation
 */
export function generateTeamLogo(team: VisualTeam): GeneratedLogo {
  return getLogoGenerator().generate(team);
}
