export const makeArray = <T>(arg: T | T[]): T[] => (Array.isArray(arg) ? arg : [arg]);

export const isEmpty = (arg: unknown): boolean => {
    if (typeof arg === 'number' || typeof arg === 'boolean') {
        return false;
    }
    if (typeof arg === 'undefined' || arg === null || arg === '') {
        return true;
    }
    if (typeof arg === 'string' || Array.isArray(arg)) {
        return arg.length === 0;
    }
    return Object.entries(arg).length === 0;
};

export const omit = <T extends Record<string, any>, K extends keyof T>(obj: T, key: K): Omit<T, K> => {
    const { [key]: _, ...rest } = obj;
    return rest;
};

export const pluralize = (number: number, text: string): string => (number === 1 ? text : `${text}s`);

export const truncate = (string: string, maxLength: number): string => (
    string.length > maxLength ? `${string.slice(0, maxLength)}...` : string
);
  
export const reduceById = <T extends { id: string }>(arr: T[]): Record<string, T> => (
    arr.reduce((acc: Record<string, T>, item) => {
        acc[item.id] = item;
        return acc;
    }, {})
);
  
  
export const reduceToIds = <T extends { id: string }>(arr: T[]): string[] => (
    arr.reduce((acc, item) => [...acc, item.id], [] as string[])
);
