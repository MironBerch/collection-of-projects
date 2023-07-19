import axios, { AxiosRequestConfig } from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

const api = async (descriptor: AxiosRequestConfig, nextUrl: string | null = null): Promise<any> => {
    const desc: AxiosRequestConfig = { ...descriptor };
    if (nextUrl) {
        desc.url = nextUrl;
    }
    const { data } = await axios(desc);
    return data;
};

export default api;

export const descriptor = {

    //
    // Post descriptors
    //

    createLike: (postId: number) => (
        {
            method: 'post',
            url: `/api/posts/${postId}/likes/`,
        }
    ),

    createPost: (data: any) => (
        {
            data,
            method: 'post',
            url: '/api/posts/',
        }
    ),

    createRepost: (data: any) => (
        {
            data,
            method: 'post',
            url: '/api/posts/repost/',
        }
    ),

    editPost: (postId: number, content: string) => (
        {
            data: {
                content,
            },
            method: 'patch',
            url: `/api/posts/${postId}/`,
        }
    ),

    getFeed: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/posts/feed/',
        }
    ),

    getLikes: (postId: number) => (
        {
            method: 'get',
            url: `/api/posts/${postId}/likes/`,
        }
    ),

    getPost: (postId: number) => (
        {
            method: 'get',
            url: `/api/posts/${postId}/`,
        }
    ),

    getPostLikes: (postId: number) => (
        {
            method: 'get',
            url: `/api/posts/${postId}/likes/`,
        }
    ),

    getPosts: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/posts/',
        }
    ),

    getProfileLikes: (username: string) => (
        {
            method: 'get',
            url: `/api/posts/profile/${username}/likes/`,
        }
    ),

    getProfilePosts: (username: string) => (
        {
            method: 'get',
            url: `/api/posts/profile/${username}/posts/`,
        }
    ),

    getLongRecommendedPosts: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/posts/long-recommended-posts/',
        }
    ),

    getRecommendedPosts: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/posts/recommended-posts/',
        }
    ),

    getReplies: (postId: number) => (
        {
            method: 'get',
            url: `/api/posts/${postId}/replies/`,
        }
    ),

    removeLike: (postId: number) => (
        {
            method: 'delete',
            url: `/api/posts/${postId}/likes/`,
        }
    ),

    removePost: (postId: number) => (
        {
            method: 'delete',
            url: `/api/posts/${postId}/`,
        }
    ),

    //
    // User descriptors
    //

    createFollow: (username: string) => (
        {
            method: 'post',
            url: `/api/accounts/${username}/following/`,
        }
    ),

    createUser: (data: any) => (
        {
            data,
            method: 'post',
            url: '/api/accounts/signup/',
        }
    ),

    editPassword: (data: any) => (
        {
            data,
            method: 'put',
            url: '/api/accounts/edit-password/',
        }
    ),

    editProfile: (data: any) => (
        {
            data,
            method: 'patch',
            url: '/api/accounts/edit-profile/',
        }
    ),

    editUser: (data: any) => (
        {
            data,
            method: 'patch',
            url: '/api/accounts/edit-user/',
        }
    ),

    getCurrentUser: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/accounts/current-user/',
        }
    ),

    getFollowers: (username: string) => (
        {
            method: 'get',
            url: `/api/accounts/${username}/followers/`,
        }
    ),

    getFollowing: (username: string) => (
        {
            method: 'get',
            url: `/api/accounts/${username}/following/`,
        }
    ),

    getLongRecommendedUsers: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/accounts/long-recommended-users/',
        }
    ),

    getRecommendedUsers: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/accounts/recommended-users/',
        }
    ),

    getUser: (username: string) => (
        {
            method: 'get',
            url: `/api/accounts/${username}/`,
        }
    ),

    loginUser: (data: any) => (
        {
            data,
            method: 'post',
            url: '/api/accounts/signin/',
        }
    ),

    logoutUser: (): AxiosRequestConfig => (
        {
            method: 'post',
            url: '/api/accounts/auth/signout/',
        }
    ),

    removeFollow: (username: string) => (
        {
            method: 'delete',
            url: `/api/accounts/${username}/following/`,
        }
    ),

    //
    // Search descriptors
    //

    getSearch: (searchString: string) => (
        {
            method: 'get',
            url: `/api/search/?search=${searchString}`,
        }
    ),

    //
    // Notifications descriptors
    //

    getNotifications: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/notifications/',
        }
    ),

    getUnreadNotificationsCount: (): AxiosRequestConfig => (
        {
            method: 'get',
            url: '/api/notifications/unread-count/',
        }
    ),

    removeNotification: (notificationId: number) => (
        {
            method: 'delete',
            url: `/api/notifications/${notificationId}/`,
        }
    ),
};