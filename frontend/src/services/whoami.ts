// src/services/user.ts
import axios from "axios";
// import { getFreshToken } from "./getFreshToken";

interface WhoAmI {
  success: boolean;
  twofa_admin: boolean;
}

let _whoami: Promise<WhoAmI> | null = null;

export async function fetchWhoAmI(): Promise<WhoAmI> {

  const token = "test" // await getFreshToken();

  if (!_whoami) {
    _whoami = axios
      .get<WhoAmI>(`${import.meta.env.VITE_API_URL}/whoami`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((r) => r.data)
      .catch((err) => {
        _whoami = null;
        throw err;
      });
  }

  return _whoami;
}
