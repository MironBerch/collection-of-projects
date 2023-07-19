export const APP_NAME: string = 'social-network';

export const route = {
    login: '/login/',
    followers: (username: string): string => `/users/${username}/followers/`,
    following: (username: string): string => `/users/${username}/following/`,
    home: '/home/',
    index: '/',
    notifications: '/notifications/',
    postDetail: (postId: string): string => `/post/${postId}/`,
    postLikes: (postId: string): string => `/post/${postId}/likes/`,
    postDetailLikes: (postId: string): string => `/post/${postId}/likes/`,
    profilePosts: (username: string): string => `/users/${username}/`,
    profileLikes: (username: string): string => `/users/${username}/likes/`,
    profileReplies: (username: string): string => `/users/${username}/replies/`,
    recommendedPosts: '/recommended-posts/',
    recommendedUsers: '/recommended-users/',
    register: '/register/',
    search: '/search/',
    settings: '/settings/',
};