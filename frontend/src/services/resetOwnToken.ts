import axios from "axios";
// import { getFreshToken } from "./getFreshToken";

/**
 * Reset own user token (self-service) via POST /token/reset/own/
 */
export async function resetOwnToken(): Promise<void> {
const token = "test" //await getFreshToken();

  await axios.post(
    `${import.meta.env.VITE_API_URL}/token/reset/own/`,
    {},
    {
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );
}