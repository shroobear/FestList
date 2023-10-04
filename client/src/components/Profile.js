import React from "react";
import { useLocation } from "react-router-dom";

function Profile() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const linked = queryParams.get("linked");

  return (
    <main>
      <div>
        {linked === "true" && (
          <p>Your Spotify account has been successfully linked.</p>
        )}
      </div>
    </main>
  );
}

export default Profile;
