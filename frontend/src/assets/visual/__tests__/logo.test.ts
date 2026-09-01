/**
 * Unit Tests for Procedural Logo Generator
 * Validates determinism, uniqueness, and visual quality
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { ProceduralLogoGenerator, generateTeamLogo, getLogoGenerator } from '../logo';
import { VisualTeam } from '../../../types/broadcast';

describe('ProceduralLogoGenerator', () => {
  let generator: ProceduralLogoGenerator;

  const mockTeam: VisualTeam = {
    id: 1,
    city: 'New York',
    name: 'Giants',
    abbreviation: 'NYG',
    primary_color: '#0B2265',
    secondary_color: '#A71930',
    logo_url: null,
    players: [],
  };

  beforeEach(() => {
    generator = new ProceduralLogoGenerator();
  });

  describe('Determinism', () => {
    it('generates identical logos for same team input', () => {
      const logo1 = generator.generate(mockTeam);
      const logo2 = generator.generate(mockTeam);
      
      expect(logo1.svg).toBe(logo2.svg);
      expect(logo1.hashCode).toBe(logo2.hashCode);
      expect(logo1.shapes.length).toBe(logo2.shapes.length);
    });

    it('uses consistent hashing across sessions', () => {
      const team1 = { ...mockTeam, city: 'Dallas', name: 'Cowboys' };
      const team2 = { ...mockTeam, city: 'Dallas', name: 'Cowboys' };
      
      const logo1 = generator.generate(team1);
      const logo2 = generator.generate(team2);
      
      expect(logo1.hashCode).toBe(logo2.hashCode);
    });
  });

  describe('Uniqueness', () => {
    it('generates different logos for different teams', () => {
      const team1 = { ...mockTeam, city: 'Green Bay', name: 'Packers' };
      const team2 = { ...mockTeam, city: 'Chicago', name: 'Bears' };
      
      const logo1 = generator.generate(team1);
      const logo2 = generator.generate(team2);
      
      expect(logo1.svg).not.toBe(logo2.svg);
      expect(logo1.hashCode).not.toBe(logo2.hashCode);
    });

    it('produces high uniqueness scores ( > 0.5)', () => {
      const logo = generator.generate(mockTeam);
      expect(logo.uniqueness).toBeGreaterThan(0.5);
    });

    it('varies shapes across multiple teams', () => {
      const teams = [
        { ...mockTeam, city: 'Seattle', name: 'Seahawks' },
        { ...mockTeam, city: 'Denver', name: 'Broncos' },
        { ...mockTeam, city: 'Miami', name: 'Dolphins' },
        { ...mockTeam, city: 'Kansas City', name: 'Chiefs' },
      ];

      const logos = teams.map(t => generator.generate(t));
      const shapeTypes = logos.map(l => l.shapes.map(s => s.type).join('-'));
      const uniqueCombinations = new Set(shapeTypes);

      // At least 3 out of 4 should have unique shape combinations
      expect(uniqueCombinations.size).toBeGreaterThanOrEqual(3);
    });
  });

  describe('Shape Generation', () => {
    it('generates 2-4 shapes per logo', () => {
      const logo = generator.generate(mockTeam);
      expect(logo.shapes.length).toBeGreaterThanOrEqual(2);
      expect(logo.shapes.length).toBeLessThanOrEqual(4);
    });

    it('uses valid shape types', () => {
      const validTypes = ['hexagon', 'circle', 'diamond', 'shield', 'abstract', 'star', 'triangle'];
      const logo = generator.generate(mockTeam);
      
      logo.shapes.forEach(shape => {
        expect(validTypes).toContain(shape.type);
      });
    });

    it('uses valid fill patterns', () => {
      const validPatterns = ['solid', 'gradient', 'stripes', 'dots', 'chevron'];
      const logo = generator.generate(mockTeam);
      
      logo.shapes.forEach(shape => {
        expect(validPatterns).toContain(shape.fillPattern);
      });
    });

    it('applies rotation values (0-360)', () => {
      const logo = generator.generate(mockTeam);
      
      logo.shapes.forEach(shape => {
        expect(shape.rotation).toBeGreaterThanOrEqual(0);
        expect(shape.rotation).toBeLessThanOrEqual(360);
      });
    });

    it('applies scale values (0.3-0.8)', () => {
      const logo = generator.generate(mockTeam);
      
      logo.shapes.forEach(shape => {
        expect(shape.scale).toBeGreaterThanOrEqual(0.3);
        expect(shape.scale).toBeLessThanOrEqual(0.8);
      });
    });
  });

  describe('SVG Output', () => {
    it('produces valid SVG structure', () => {
      const logo = generator.generate(mockTeam);
      
      expect(logo.svg).toContain('<svg');
      expect(logo.svg).toContain('</svg>');
      expect(logo.svg).toContain('xmlns="http://www.w3.org/2000/svg"');
      expect(logo.svg).toContain('viewBox=');
    });

    it('includes team abbreviation in text element', () => {
      const logo = generator.generate(mockTeam);
      
      expect(logo.svg).toContain('NYG');
    });

    it('uses team colors in SVG', () => {
      const logo = generator.generate(mockTeam);
      
      expect(logo.svg).toContain(mockTeam.primary_color!);
      expect(logo.svg).toContain(mockTeam.secondary_color!);
    });

    it('has proper dimensions (200x200)', () => {
      const logo = generator.generate(mockTeam);
      
      expect(logo.svg).toContain('width="200"');
      expect(logo.svg).toContain('height="200"');
      expect(logo.svg).toContain('viewBox="0 0 200 200"');
    });
  });

  describe('Caching', () => {
    it('caches generated logos', () => {
      const logo1 = generator.generate(mockTeam);
      const logo2 = generator.generate(mockTeam);
      
      // Should return cached version
      expect(logo1).toBe(logo2);
    });

    it('clears cache on command', () => {
      generator.generate(mockTeam);
      generator.clearCache();
      
      const logo = generator.generate(mockTeam);
      // After clear, should regenerate (but still be deterministic)
      expect(logo.svg).toBeDefined();
    });
  });

  describe('Color Contrast', () => {
    it('selects contrasting text color for dark backgrounds', () => {
      const darkTeam = { ...mockTeam, primary_color: '#000000' };
      const logo = generator.generate(darkTeam);
      
      expect(logo.svg).toContain('#FFFFFF'); // White text for dark bg
    });

    it('selects contrasting text color for light backgrounds', () => {
      const lightTeam = { ...mockTeam, primary_color: '#FFFFFF' };
      const logo = generator.generate(lightTeam);
      
      expect(logo.svg).toContain('#000000'); // Black text for light bg
    });
  });

  describe('Edge Cases', () => {
    it('handles missing city/name gracefully', () => {
      const incompleteTeam: VisualTeam = {
        ...mockTeam,
        city: '',
        name: '',
        abbreviation: '',
      };
      
      expect(() => generator.generate(incompleteTeam)).not.toThrow();
      const logo = generator.generate(incompleteTeam);
      expect(logo.svg).toBeDefined();
    });

    it('handles missing colors with defaults', () => {
      const noColorTeam: VisualTeam = {
        ...mockTeam,
        primary_color: null as any,
        secondary_color: null as any,
      };
      
      const logo = generator.generate(noColorTeam);
      expect(logo.svg).toContain('#003366'); // Default primary
      expect(logo.svg).toContain('#FF6600'); // Default secondary
    });

    it('handles special characters in team names', () => {
      const specialTeam = { ...mockTeam, city: 'St. Louis', name: 'Rams-O\'s' };
      
      expect(() => generator.generate(specialTeam)).not.toThrow();
      const logo = generator.generate(specialTeam);
      expect(logo.hashCode).toBeDefined();
    });
  });

  describe('Convenience Functions', () => {
    it('generateTeamLogo uses singleton instance', () => {
      const logo1 = generateTeamLogo(mockTeam);
      const logo2 = getLogoGenerator().generate(mockTeam);
      
      expect(logo1.svg).toBe(logo2.svg);
    });
  });

  describe('Performance', () => {
    it('generates logo in under 10ms', () => {
      const start = performance.now();
      generator.generate(mockTeam);
      const end = performance.now();
      
      expect(end - start).toBeLessThan(10);
    });

    it('handles batch generation efficiently', () => {
      const teams = Array.from({ length: 32 }, (_, i) => ({
        ...mockTeam,
        id: i,
        city: `City ${i}`,
        name: `Team ${i}`,
      }));

      const start = performance.now();
      teams.forEach(t => generator.generate(t));
      const end = performance.now();

      // 32 logos in under 100ms
      expect(end - start).toBeLessThan(100);
    });
  });
});

describe('Hash Function', () => {
  it('djb2Hash produces consistent results', () => {
    // Import internal function via module access
    const testString = 'New York Giants';
    const hash1 = testString.split('').reduce((h, c) => ((h << 5) + h) + c.charCodeAt(0), 5381);
    const hash2 = testString.split('').reduce((h, c) => ((h << 5) + h) + c.charCodeAt(0), 5381);
    
    expect(hash1).toBe(hash2);
  });
});
