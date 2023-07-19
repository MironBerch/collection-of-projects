import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { getUser, key, selectProfileUser, RootState } from '../redux/profile';

import useUI from './useUI';

const useProfileUser = (slug: string) => {
    const dispatch = useDispatch();

    const profileUser = useSelector((s: RootState) => selectProfileUser(s, slug));

    const {
        fetched,
        loading: profileUserLoading,
    } = useUI(key.profileUser(slug));

    useEffect(() => {
        if (!fetched) {
            dispatch(getUser(slug));
        }
    }, [dispatch, fetched, slug]);

    return { profileUser, profileUserLoading };
};

export default useProfileUser;
