

export async function checkIfArtistExists(artistName) {
  const response = await fetch(`/v1/artists/search/${artistName}`);
  if (response.ok) {
    const data = await response.json();
    return data;
  } else if (response.status === 404) {
    return null;
  }
  throw new Error("Failed to check artist.");
}

export async function createArtist(artistData) {
  const response = await fetch(`/v1/artists`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({name: artistData.name, spotify_id: artistData.id}),
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  }
  throw new Error("Failed to create artist.");
}

export async function checkIfInLineup(festival_id, artistId) {
  const response = await fetch(
    `/v1/lineups/pair/${festival_id}/${artistId}`
  );
  if (response.ok) {
    const data = await response.json();
    return data;
  } else if (response.status === 404) {
    return null;
  }
  throw new Error("Failed to check lineup.");
}

export async function addToLineup(festival_id, artistId) {
  const response = await fetch(`/v1/lineups/pair/${festival_id}/${artistId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  }
  throw new Error("Failed to add to lineup.");
}

export const usStates = [
  "AL",
  "AK",
  "AZ",
  "AR",
  "CA",
  "CO",
  "CT",
  "DE",
  "FL",
  "GA",
  "HI",
  "ID",
  "IL",
  "IN",
  "IA",
  "KS",
  "KY",
  "LA",
  "ME",
  "MD",
  "MA",
  "MI",
  "MN",
  "MS",
  "MO",
  "MT",
  "NE",
  "NV",
  "NH",
  "NJ",
  "NM",
  "NY",
  "NC",
  "ND",
  "OH",
  "OK",
  "OR",
  "PA",
  "RI",
  "SC",
  "SD",
  "TN",
  "TX",
  "UT",
  "VT",
  "VA",
  "WA",
  "WV",
  "WI",
  "WY",
];