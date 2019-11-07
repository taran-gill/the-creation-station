class Connection {
    static getApiServer = () => {
        if (process.env.NODE_ENV === 'development') {
            return `http://${window.location.hostname}:${process.env.REACT_APP_API_PORT}`;
        }

        // TODO: In production, get api server from environment variable
        return null;
    }
}

export { Connection as default, Connection };