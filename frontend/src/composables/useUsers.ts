import { ref } from "vue";
import { type UserData } from "../types";

export function useUsers() {
  const users = ref<UserData[]>([]);
  const loading = ref(true);
  const error = ref<Error | null>(null);

  const fetchUsers = async () => {
    loading.value = true;
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/list_users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${import.meta.env.VITE_API_TOKEN}`,
        },
        body: JSON.stringify({
          user_ids: ["f:353a4f09-62c1-4f8d-8e22-b9a1b04f8b6e:yschmidt"],
        }),
      });

      const data = await response.json();
      console.log("Response data:", data);
      users.value = data.users ?? [];
    } catch (err: any) {
      error.value = err;
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    loading,
    error,
    fetchUsers,
  };
}
