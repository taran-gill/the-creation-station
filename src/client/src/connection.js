let hostname = null;
if (process.env.NODE_ENV === 'development') {
    hostname = `https://${window.location.hostname}:${process.env.REACT_APP_API_PORT}`;
}

class Connection {
    static get = async (path) => {
        const response = await fetch(hostname + path);

        if (!response.ok) {
            return null;
        }

        return response.text();
    }

    static put = async (path, body) => {
        const response = await fetch(hostname + path, { method: 'POST', body });

        if (!response.ok) {
            return null;
        }

        return response.text();
    }
}

export { Connection as default, Connection };