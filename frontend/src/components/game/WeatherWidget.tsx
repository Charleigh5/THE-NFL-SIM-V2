import React from "react";
import "./WeatherWidget.css";

interface WeatherWidgetProps {
  temperature: number;
  condition: string;
  windSpeed: number;
  location?: string;
}

export const WeatherWidget: React.FC<WeatherWidgetProps> = ({
  temperature,
  condition,
  windSpeed,
  location,
}) => {
  const getWeatherIcon = (cond: string) => {
    const c = cond.toLowerCase();
    if (c.includes("rain")) return "🌧️";
    if (c.includes("snow")) return "❄️";
    if (c.includes("cloud")) return "☁️";
    if (c.includes("clear") || c.includes("sun")) return "☀️";
    return "🌤️";
  };

  const getImpactDescription = () => {
    const impacts = [];
    if (temperature < 32) impacts.push("Ball Hardness (Fumbles ↑)");
    if (temperature > 90) impacts.push("Heat Fatigue (Stamina ↓)");
    if (windSpeed > 15) impacts.push("High Winds (Passing/Kicking ↓)");
    if (condition.toLowerCase().includes("rain")) impacts.push("Slippery Field (Cuts/Catching ↓)");
    if (condition.toLowerCase().includes("snow")) impacts.push("Poor Visibility (Passing ↓)");

    if (impacts.length === 0) return "Ideal Conditions";
    return impacts.join(" • ");
  };

  return (
    <div className="weather-widget">
      <div className="weather-header">
        <span className="weather-location">{location || "Stadium Weather"}</span>
      </div>
      <div className="weather-main">
        <div className="weather-icon">{getWeatherIcon(condition)}</div>
        <div className="weather-temp">{temperature}°F</div>
      </div>
      <div className="weather-details">
        <div className="detail-item">
          <span className="label">Condition</span>
          <span className="value">{condition}</span>
        </div>
        <div className="detail-item">
          <span className="label">Wind</span>
          <span className="value">{windSpeed} mph</span>
        </div>
      </div>
      <div className="weather-impact">
        <span className="impact-label">Gameplay Impact:</span>
        <span className="impact-value">{getImpactDescription()}</span>
      </div>
    </div>
  );
};
