export function generateRandomString(length: number) {
    // Character set from which to generate the random string
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let randomString = '';

    // Loop to generate each character in the string
    for (let i = 0; i < length; i++) {
        // Generate a random index within the character set
        const randomIndex = Math.floor(Math.random() * charset.length);
        // Append the character at the random index to the random string
        randomString += charset[randomIndex];
    }

    return randomString;
}