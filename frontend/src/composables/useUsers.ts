import { ref } from "vue";
import { type UserData } from "../types";

export function useUsers() {
  const users = ref<UserData[]>([]);
  const loading = ref(true);
  const error = ref<Error | null>(null);

  const initialPerPage = 20;
  const currentPage = ref(1);
  const perPage = ref(initialPerPage);
  const totalPages = ref(1);

  const fetchUsers = async (page = 0) => {
    loading.value = true;
    console.log("Fetching users...", page);
    const params = new URLSearchParams({
      page:  String(page - 1),
      limit: String(perPage.value),
    }).toString();
    
    const endpoint = `${import.meta.env.VITE_API_URL}/list_users?${params}`;
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${import.meta.env.VITE_API_TOKEN}`,
        },
      });

      const data = await response.json();
      console.log("Response data:", data);
      users.value = data.users ?? [];

      totalPages.value = data.total_pages ?? 1;
      currentPage.value = page;

    } catch (err: any) {
      error.value = err;
      console.error("Error fetching users:", err);
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    loading,
    error,
    currentPage,
    totalPages,
    perPage,
    fetchUsers,
  };
}
