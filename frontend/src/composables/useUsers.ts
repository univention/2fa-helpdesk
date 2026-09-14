/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2026 Univention GmbH
 */

import { computed, ref, watch } from "vue";
import axiosInstance from "../services/axios";
import { getUsersResponseData, type UserData } from "../types";

/** Shortest search term we are willing to send to the backend. */
export const MIN_SEARCH_LENGTH = 3;

export function useUsers() {
  const users = ref<UserData[]>([]);
  const loading = ref(true);
  const loadingMore = ref(false);
  const error = ref<Error | null>(null);

  const searchQuery = ref("");
  const initialPerPage = 10;
  const currentPage = ref(1);
  const perPage = ref(initialPerPage);
  const hasNextPage = ref(false);

  // One or two characters match far too much to be worth the LDAP lookup, so
  // those are not sent at all. An empty query is fine, that lists the first page.
  const searchTooShort = computed(
    () =>
      searchQuery.value.length > 0 &&
      searchQuery.value.length < MIN_SEARCH_LENGTH
  );

  // Only the most recent request may write to the state. Without this a slow
  // response for an earlier search term could append its rows onto the results
  // of a newer one.
  let latestRequestId = 0;

  // whenever the search string changes, re-fetch page 1
  watch(searchQuery, () => {
    if (searchTooShort.value) {
      // Invalidate whatever is in flight so it cannot land afterwards.
      latestRequestId++;
      loading.value = false;
      loadingMore.value = false;
      return;
    }
    fetchUsers(1);
  });

  const fetchUsers = async (page = 1, append = false) => {
    const requestId = ++latestRequestId;
    const isStale = () => requestId !== latestRequestId;

    if (append) {
      loadingMore.value = true;
    } else {
      loading.value = true;
    }
    error.value = null;

    try {
      const response: getUsersResponseData = await axiosInstance.post(
        "/list_users",
        { query: searchQuery.value },
        {
          params: {
            page: page,
            limit: perPage.value,
          },
        }
      );

      if (isStale()) return;

      const data = response.data;
      const pageUsers = data.users ?? [];

      users.value = append ? [...users.value, ...pageUsers] : pageUsers;
      hasNextPage.value = data.has_next ?? false;
      currentPage.value = page;
    } catch (err: any) {
      if (isStale()) return;
      error.value = err;
      console.error("Error fetching users:", err);
    } finally {
      if (!isStale()) {
        loading.value = false;
        loadingMore.value = false;
      }
    }
  };

  // Appends the next page. currentPage only advances once a request succeeded,
  // so a failed load can simply be retried.
  const loadMore = () => {
    if (searchTooShort.value) return;
    if (!hasNextPage.value || loading.value || loadingMore.value) return;
    fetchUsers(currentPage.value + 1, true);
  };

  return {
    users,
    searchQuery,
    searchTooShort,
    loading,
    loadingMore,
    error,
    currentPage,
    hasNextPage,
    perPage,
    fetchUsers,
    loadMore,
  };
}
