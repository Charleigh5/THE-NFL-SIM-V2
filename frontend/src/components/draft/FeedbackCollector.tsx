import React, { useState } from "react";
import "./FeedbackCollector.css";

interface FeedbackCollectorProps {
  contextId: string; // ID of the recommendation (e.g., draft pick ID or trade ID)
  contextType: "draft" | "trade";
  onFeedbackSubmit?: (feedback: FeedbackData) => void;
}

export interface FeedbackData {
  contextId: string;
  contextType: "draft" | "trade";
  isHelpful: boolean;
  comment?: string;
}

export const FeedbackCollector: React.FC<FeedbackCollectorProps> = ({
  contextId,
  contextType,
  onFeedbackSubmit,
}) => {
  const [isHelpful, setIsHelpful] = useState<boolean | null>(null);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleVote = (vote: boolean) => {
    setIsHelpful(vote);
    // If voting "helpful" and no comment needed, we could auto-submit,
    // but for now let's keep it explicit or just set state.
  };

  const handleSubmit = async () => {
    if (isHelpful === null) return;

    setIsSubmitting(true);

    const feedback: FeedbackData = {
      contextId,
      contextType,
      isHelpful,
      comment: comment.trim(),
    };

    try {
      const response = await fetch("/api/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(feedback),
      });

      if (!response.ok) {
        throw new Error("Failed to submit feedback");
      }

      if (onFeedbackSubmit) {
        onFeedbackSubmit(feedback);
      }

      setSubmitted(true);
    } catch (error) {
      console.error("Error submitting feedback:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="feedback-collector">
        <div className="feedback-success">Thanks for your feedback!</div>
      </div>
    );
  }

  return (
    <div className="feedback-collector">
      <div className="feedback-header">Was this recommendation helpful?</div>

      <div className="feedback-actions">
        <button
          className={`feedback-btn ${isHelpful === true ? "active" : ""}`}
          onClick={() => handleVote(true)}
        >
          👍 Yes
        </button>
        <button
          className={`feedback-btn ${isHelpful === false ? "active" : ""}`}
          onClick={() => handleVote(false)}
        >
          👎 No
        </button>
      </div>

      {isHelpful !== null && (
        <div className="feedback-comment">
          <textarea
            placeholder="Any additional comments? (Optional)"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
          <button className="submit-feedback-btn" onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting ? "Sending..." : "Submit Feedback"}
          </button>
        </div>
      )}
    </div>
  );
};
