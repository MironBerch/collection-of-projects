import { useEffect } from 'react';

const useLogChanged = (keyValue: Record<string, any>) => {
    const [[key, value]] = Object.entries(keyValue);

    useEffect(() => {
        console.log(`Change detected for "${key}"`);
    }, [key, value]);
};

export default useLogChanged;