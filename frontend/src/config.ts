// 获取后端服务器地址
export const getBackendURL = () => {
  // 如果在环境变量中配置了后端地址，使用配置的地址
  const configuredURL = (import.meta as any).env?.VITE_BACKEND_URL;
  if (configuredURL) {
    return configuredURL;
  }
  
  // 否则根据当前主机名自动判断
  const hostname = window.location.hostname;
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  
  // 如果是 localhost，使用 localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'ws://localhost:8000';
  }
  
  // 生产环境：通过 Nginx 代理，使用相对路径
  // Docker 部署时，前端和后端在同一域名下
  return `${protocol}//${hostname}`;
};

export const getBackendHTTPURL = () => {
  const wsURL = getBackendURL();
  return wsURL.replace('wss://', 'https://').replace('ws://', 'http://');
};
