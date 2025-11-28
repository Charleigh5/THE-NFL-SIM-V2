/**
 * ImageGenService: Handles AI Image Generation (Nano Banana Pro)
 * NOTE: This is currently a MOCK implementation. Replace with real API calls when ready.
 */

export interface GameEvent {
  type: "touchdown" | "interception" | "fumble" | "field_goal" | "safety";
  player: string;
  team: string;
  weather?: string;
  quarter?: number;
}

export interface GeneratedImage {
  url: string;
  prompt: string;
  timestamp: number;
}

class ImageGenServiceClass {
  private mockImages = [
    "https://images.unsplash.com/photo-1566577739112-5180d4bf9390?w=800&q=80", // Football field
    "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&q=80", // Stadium
    "https://images.unsplash.com/photo-1577223625816-7546f762303c?w=800&q=80", // Action
  ];

  /**
   * Constructs a detailed prompt from a game event
   */
  constructPrompt(event: GameEvent): string {
    const { type, player, team, weather } = event;

    const weatherDesc = weather ? `, ${weather} conditions` : "";
    const styleTag =
      "cinematic wide shot, hyper-realistic, cyberpunk aesthetic, dramatic lighting";

    const eventDescriptions = {
      touchdown: `futuristic football player ${player} in ${team} armor scoring a touchdown`,
      interception: `defensive player ${player} in ${team} uniform intercepting the ball mid-air`,
      fumble: `intense fumble recovery by ${player} of ${team}`,
      field_goal: `kicker ${player} of ${team} executing a game-winning field goal`,
      safety: `dramatic safety tackle by ${player} in ${team} colors`,
    };

    return `${eventDescriptions[type]}${weatherDesc}, ${styleTag}`;
  }

  /**
   * Generates an image (MOCK: returns a random placeholder)
   */
  async generateImage(prompt: string): Promise<GeneratedImage> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Return mock image
    const url =
      this.mockImages[Math.floor(Math.random() * this.mockImages.length)];

    return {
      url,
      prompt,
      timestamp: Date.now(),
    };
  }

  /**
   * High-level method: Generate from event
   */
  async generateFromEvent(event: GameEvent): Promise<GeneratedImage> {
    const prompt = this.constructPrompt(event);
    console.log("[ImageGenService] Generating image with prompt:", prompt);
    return this.generateImage(prompt);
  }
}

export const ImageGenService = new ImageGenServiceClass();
