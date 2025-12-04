import React from "react";
import type { GameWeather } from "../../types/season";
import "./WeatherWidget.css";

interface WeatherWidgetProps {
  weather: GameWeather;
  location?: string;
}

export const WeatherWidget: React.FC<WeatherWidgetProps> = ({ weather, location }) => {
  const getConditionText = () => {
    if (weather.precipitation_type && weather.precipitation_type !== "None") {
      return weather.precipitation_type;
    }
    // Could infer from cloud cover if available, otherwise default
    return "Clear";
  };

  const condition = getConditionText();

  const getWeatherIcon = (cond: string) => {
    const c = cond.toLowerCase();
    if (c.includes("rain")) return "🌧️";
    if (c.includes("snow")) return "❄️";
    if (c.includes("sleet")) return "🌨️";
    if (c.includes("cloud")) return "☁️";
    return "☀️";
  };

  const getImpactDescription = () => {
    const impacts = [];
    if (weather.temperature < 32) impacts.push("Cold (Fumbles ↑)");
    if (weather.temperature > 90) impacts.push("Heat (Fatigue ↑)");
    if (weather.wind_speed > 15) impacts.push("Wind (Passing/Kicking ↓)");

    if (weather.field_condition === "Wet" || weather.field_condition === "Muddy") {
      impacts.push("Slippery (Cuts ↓)");
    }
    if (weather.field_condition === "Snowy") {
      impacts.push("Snow (Visibility ↓)");
    }

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
        <div className="weather-temp">{Math.round(weather.temperature)}°F</div>
      </div>
      <div className="weather-details">
        <div className="detail-item">
          <span className="label">Condition</span>
          <span className="value">{condition}</span>
        </div>
        <div className="detail-item">
          <span className="label">Wind</span>
          <span className="value">
            {Math.round(weather.wind_speed)} mph {weather.wind_direction}
          </span>
        </div>
        <div className="detail-item">
          <span className="label">Field</span>
          <span className="value">{weather.field_condition || "Dry"}</span>
        </div>
      </div>
      <div className="weather-impact">
        <span className="impact-label">Impact:</span>
        <span className="impact-value">{getImpactDescription()}</span>
      </div>
    </div>
  );
};
