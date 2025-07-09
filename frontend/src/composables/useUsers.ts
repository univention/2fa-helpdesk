/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { ref, watch } from "vue";
import axiosInstance from "../services/axios";
import { type UserData } from "../types";

export function useUsers() {
  const users = ref<UserData[]>([]);
  const loading = ref(true);
  const error = ref<Error | null>(null);

  const searchQuery = ref("");
  const initialPerPage = 20;
  const currentPage = ref(1);
  const perPage = ref(initialPerPage);
  const totalPages = ref(1);

  // whenever the search string changes, re-fetch page 1
  watch(searchQuery, () => {
    fetchUsers(1);
  });

  const fetchUsers = async (page = 1) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await axiosInstance.post(
        "/list_users",
        { query: searchQuery.value },
        {
          params: {
            page: page,
            limit: perPage.value,
          },
        }
      );

      const data = response.data;
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
    searchQuery,
    loading,
    error,
    currentPage,
    totalPages,
    perPage,
    fetchUsers,
  };
}
