/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2026 Univention GmbH
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { nextTick } from "vue";
import axiosInstance from "@/services/axios";
import { useUsers } from "@/composables/useUsers";
import type { UserData } from "@/types";

const PAGE_SIZE = 10;

function makeUser(n: number): UserData {
  return {
    username: `user-${n}`,
    firstname: `First${n}`,
    lastname: `Last${n}`,
    email: `user-${n}@example.com`,
    keycloak_internal_id: `id-${n}`,
    totp: null,
  };
}

function makePage(from: number, count: number, hasNext: boolean) {
  return {
    data: {
      users: Array.from({ length: count }, (_, i) => makeUser(from + i)),
      success: true,
      has_next: hasNext,
      page: 1,
      limit: PAGE_SIZE,
      detail: "",
    },
  };
}

/** Query string of the nth call to the endpoint. */
function queryOf(postMock: any, call: number) {
  return postMock.mock.calls[call][1].query;
}

/** Page/limit params of the nth call to the endpoint. */
function paramsOf(postMock: any, call: number) {
  return postMock.mock.calls[call][2].params;
}

describe("useUsers", () => {
  let postMock: any;

  beforeEach(() => {
    postMock = vi.spyOn(axiosInstance, "post");
  });

  afterEach(() => {
    postMock.mockRestore();
  });

  describe("fetching", () => {
    it("requests the first page with the configured page size", async () => {
      postMock.mockResolvedValue(makePage(1, PAGE_SIZE, true));
      const { users, hasNextPage, loading, fetchUsers } = useUsers();

      await fetchUsers();

      expect(postMock).toHaveBeenCalledTimes(1);
      expect(paramsOf(postMock, 0)).toEqual({ page: 1, limit: PAGE_SIZE });
      expect(users.value).toHaveLength(PAGE_SIZE);
      expect(hasNextPage.value).toBe(true);
      expect(loading.value).toBe(false);
    });

    it("reports when no further page is available", async () => {
      postMock.mockResolvedValue(makePage(1, 3, false));
      const { hasNextPage, fetchUsers } = useUsers();

      await fetchUsers();

      expect(hasNextPage.value).toBe(false);
    });
  });

  describe("loading more", () => {
    it("appends the next page instead of replacing the current one", async () => {
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { users, currentPage, fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      postMock.mockResolvedValueOnce(makePage(11, PAGE_SIZE, false));
      await loadMore();

      expect(paramsOf(postMock, 1)).toEqual({ page: 2, limit: PAGE_SIZE });
      expect(users.value).toHaveLength(2 * PAGE_SIZE);
      expect(users.value[0].username).toBe("user-1");
      expect(users.value[PAGE_SIZE].username).toBe("user-11");
      expect(currentPage.value).toBe(2);
    });

    it("keeps the loaded rows visible while the next page is in flight", async () => {
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { users, loading, loadingMore, fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      let resolveSecond: (value: unknown) => void;
      postMock.mockReturnValueOnce(
        new Promise((resolve) => {
          resolveSecond = resolve;
        })
      );

      const pending = loadMore();
      await nextTick();

      // The table renders its "loading" placeholder off `loading`, so that one
      // has to stay false or the rows already on screen would be replaced.
      expect(loading.value).toBe(false);
      expect(loadingMore.value).toBe(true);
      expect(users.value).toHaveLength(PAGE_SIZE);

      resolveSecond!(makePage(11, 5, false));
      await pending;

      expect(loadingMore.value).toBe(false);
      expect(users.value).toHaveLength(PAGE_SIZE + 5);
    });

    it("does nothing when there is no further page", async () => {
      postMock.mockResolvedValue(makePage(1, 3, false));
      const { fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      await loadMore();

      expect(postMock).toHaveBeenCalledTimes(1);
    });

    it("stays on the same page when loading more failed, so it can be retried", async () => {
      vi.spyOn(console, "error").mockImplementation(() => {});
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { users, currentPage, error, fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      postMock.mockRejectedValueOnce(new Error("boom"));
      await loadMore();

      expect(error.value).toBeInstanceOf(Error);
      expect(currentPage.value).toBe(1);
      expect(users.value).toHaveLength(PAGE_SIZE);

      postMock.mockResolvedValueOnce(makePage(11, PAGE_SIZE, false));
      await loadMore();

      expect(paramsOf(postMock, 2)).toEqual({ page: 2, limit: PAGE_SIZE });
      expect(users.value).toHaveLength(2 * PAGE_SIZE);
    });
  });

  describe("search", () => {
    it("does not query a term shorter than the minimum length", async () => {
      const { searchQuery, searchTooShort } = useUsers();

      searchQuery.value = "ab";
      await nextTick();

      expect(searchTooShort.value).toBe(true);
      expect(postMock).not.toHaveBeenCalled();
    });

    it("queries again once the term reaches the minimum length", async () => {
      postMock.mockResolvedValue(makePage(1, 2, false));
      const { searchQuery, searchTooShort } = useUsers();

      searchQuery.value = "ab";
      await nextTick();
      searchQuery.value = "abcde";
      await nextTick();
      await vi.waitFor(() => expect(postMock).toHaveBeenCalledTimes(1));

      expect(searchTooShort.value).toBe(false);
      expect(queryOf(postMock, 0)).toBe("abcde");
      expect(paramsOf(postMock, 0)).toEqual({ page: 1, limit: PAGE_SIZE });
    });

    it("treats an emptied search field as an unfiltered listing", async () => {
      postMock.mockResolvedValue(makePage(1, PAGE_SIZE, true));
      const { searchQuery } = useUsers();

      searchQuery.value = "abcde";
      await nextTick();
      await vi.waitFor(() => expect(postMock).toHaveBeenCalledTimes(1));

      searchQuery.value = "";
      await nextTick();
      await vi.waitFor(() => expect(postMock).toHaveBeenCalledTimes(2));

      expect(queryOf(postMock, 1)).toBe("");
    });

    it("restarts from the first page and drops the previous results", async () => {
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { users, currentPage, searchQuery, fetchUsers, loadMore } = useUsers();
      await fetchUsers();
      postMock.mockResolvedValueOnce(makePage(11, PAGE_SIZE, true));
      await loadMore();
      expect(currentPage.value).toBe(2);

      postMock.mockResolvedValueOnce(makePage(50, 2, false));
      searchQuery.value = "abcde";
      await nextTick();
      await vi.waitFor(() => expect(users.value).toHaveLength(2));

      expect(currentPage.value).toBe(1);
      expect(users.value[0].username).toBe("user-50");
    });

    it("refuses to load more while the term is too short to be queried", async () => {
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { searchQuery, fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      searchQuery.value = "ab";
      await nextTick();
      await loadMore();

      expect(postMock).toHaveBeenCalledTimes(1);
    });
  });

  describe("out of order responses", () => {
    it("ignores a response that a newer request has superseded", async () => {
      let resolveStale: (value: unknown) => void;
      postMock.mockReturnValueOnce(
        new Promise((resolve) => {
          resolveStale = resolve;
        })
      );

      const { users, hasNextPage, loading, searchQuery, fetchUsers } = useUsers();
      fetchUsers();
      await nextTick();

      // A newer search overtakes the still pending first request.
      postMock.mockResolvedValueOnce(makePage(50, 1, false));
      searchQuery.value = "abcde";
      await nextTick();
      await vi.waitFor(() => expect(users.value).toHaveLength(1));

      resolveStale!(makePage(1, PAGE_SIZE, true));
      await nextTick();
      await nextTick();

      expect(users.value).toHaveLength(1);
      expect(users.value[0].username).toBe("user-50");
      expect(hasNextPage.value).toBe(false);
      expect(loading.value).toBe(false);
    });

    it("does not append a stale page onto a newer result", async () => {
      postMock.mockResolvedValueOnce(makePage(1, PAGE_SIZE, true));
      const { users, searchQuery, fetchUsers, loadMore } = useUsers();
      await fetchUsers();

      let resolveStalePage: (value: unknown) => void;
      postMock.mockReturnValueOnce(
        new Promise((resolve) => {
          resolveStalePage = resolve;
        })
      );
      loadMore();
      await nextTick();

      postMock.mockResolvedValueOnce(makePage(50, 2, false));
      searchQuery.value = "abcde";
      await nextTick();
      await vi.waitFor(() => expect(users.value).toHaveLength(2));

      resolveStalePage!(makePage(11, PAGE_SIZE, true));
      await nextTick();
      await nextTick();

      expect(users.value).toHaveLength(2);
      expect(users.value.map((user) => user.username)).toEqual([
        "user-50",
        "user-51",
      ]);
    });
  });
});
