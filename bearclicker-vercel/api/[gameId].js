const fs = require('fs');
const path = require('path');

// 读取游戏配置文件
let config;
try {
  const configPath = path.join(process.cwd(), 'config', 'games.json');
  console.log(`读取配置文件: ${configPath}`);
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  console.log(`配置加载成功, 包含 ${config.games.length} 个游戏`);
} catch (error) {
  console.error(`加载配置文件失败: ${error.message}`);
  config = { games: [], brandName: 'Bear Clicker', brandUrl: 'https://bearclicker.net' };
}

// 读取游戏模板文件
let templateContent;
try {
  const templatePath = path.join(process.cwd(), 'public', 'game-template.html');
  console.log(`读取模板文件: ${templatePath}`);
  templateContent = fs.readFileSync(templatePath, 'utf8');
  console.log('模板加载成功');
} catch (error) {
  console.error(`加载模板文件失败: ${error.message}`);
  templateContent = '<!DOCTYPE html><html><body><h1>Error loading template</h1></body></html>';
}

/**
 * 处理游戏请求的API路由函数
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 */
module.exports = (req, res) => {
  try {
    // 记录请求信息
    console.log(`\n--- 新请求 ---`);
    console.log(`请求URL: ${req.url}`);
    console.log(`请求方法: ${req.method}`);
    console.log(`请求域名: ${req.headers.host}`);
    console.log(`Referer: ${req.headers.referer || 'none'}`);
    console.log(`User-Agent: ${req.headers['user-agent']}`);
    
    // 获取请求的游戏ID
    const { gameId } = req.query;
    console.log(`原始游戏ID: ${gameId}`);
    
    // 检查是否是.embed格式的请求
    const isEmbedRequest = gameId && gameId.endsWith('.embed');
    console.log(`是否为embed请求: ${isEmbedRequest}`);
    
    // 清理游戏ID，移除.html或.embed后缀和非法字符
    const gameIdClean = gameId ? gameId.replace(/\.(html|embed)$/, '').replace(/[^a-zA-Z0-9-_]/g, '') : '';
    console.log(`清理后的游戏ID: ${gameIdClean}`);
    
    // 查找游戏配置
    const gameConfig = config.games.find(g => g.id === gameIdClean);
    
    // 如果找不到游戏配置，返回404
    if (!gameConfig) {
      console.log(`未找到游戏配置: ${gameIdClean}`);
      return res.status(404).send(`Game not found: ${gameIdClean}`);
    }
    
    console.log(`找到游戏: ${gameConfig.title}`);
    console.log(`游戏URL: ${gameConfig.url}`);
    
    // 如果是.embed请求，直接重定向到游戏URL
    if (isEmbedRequest) {
      console.log(`处理embed请求，重定向到: ${gameConfig.url}`);
      res.setHeader('Location', gameConfig.url);
      return res.status(302).end();
    }
    
    // 替换模板中的占位符
    let html = templateContent
      .replace(/{{GAME_TITLE}}/g, gameConfig.title)
      .replace(/{{GAME_URL}}/g, gameConfig.url)
      .replace(/{{DOMAIN_DISPLAY}}/g, config.brandName || 'Bear Clicker')
      .replace(/{{DOMAIN_LINK}}/g, config.brandUrl || 'https://bearclicker.net');
    
    // 添加调试信息到HTML（仅在开发环境）
    if (process.env.NODE_ENV !== 'production') {
      const debugInfo = `
        <!-- Debug Info:
        Request URL: ${req.url}
        Game ID: ${gameIdClean}
        Game Title: ${gameConfig.title}
        Game URL: ${gameConfig.url}
        Host: ${req.headers.host}
        Timestamp: ${new Date().toISOString()}
        -->
      `;
      html = html.replace('</head>', `${debugInfo}</head>`);
    }
    
    // 设置响应头部
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=14400, s-maxage=2592000');
    console.log('响应准备完成，发送HTML');
    
    // 发送响应
    res.status(200).send(html);
  } catch (error) {
    console.error(`处理请求时出错: ${error.message}`);
    console.error(error.stack);
    res.status(500).send(`Internal Server Error: ${error.message}`);
  }
};
