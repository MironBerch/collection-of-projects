import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { selectErrors, selectFetched, selectLoading } from '../redux/ui';

const useUI = (
    key: string,
    keyNext?: string,
    initialLoading = true
) => {
    const errors = useSelector((state: RootState) => selectErrors(state, key));
    const fetched = useSelector((state: RootState) => selectFetched(state, key));
    const loading = useSelector((state: RootState) =>
        selectLoading(state, key, initialLoading)
    );
    const nextLoading = useSelector((state: RootState) =>
        keyNext ? selectLoading(state, keyNext) : false
    );

    return {
        errors,
        fetched,
        loading,
        nextLoading,
    };
};

export default useUI;
