# Simple Test Project - Task Completion Checklist

**Project Location**: `/home/james/test-simple-project/`
**Session**: `simple-test`
**Agent Window**: `simple-test:0`

## Task Breakdown & Verification

### Task 1: Add /status Endpoint
- [ ] **Implementation**: Add URL routing to handle `/status` requests
- [ ] **Response Format**: Return JSON: `{"status": "ok", "timestamp": "2025-09-11T17:30:00.000Z"}`
- [ ] **Test Command**: `curl http://localhost:3000/status`
- [ ] **Expected**: Valid JSON response with current timestamp

### Task 2: Add Basic Error Handling
- [ ] **Implementation**: Wrap server logic in try-catch blocks
- [ ] **Error Responses**: Return proper HTTP error codes (404, 500, etc.)
- [ ] **Crash Prevention**: Handle uncaught exceptions gracefully
- [ ] **Test Command**: Try invalid requests, check server doesn't crash
- [ ] **Expected**: Server remains running even with errors

### Task 3: Create Simple HTML Response
- [ ] **Implementation**: Return HTML content for root path `/`
- [ ] **Format**: Simple HTML page (can be basic but must be HTML, not plain text)
- [ ] **Test Command**: `curl http://localhost:3000/` or open in browser
- [ ] **Expected**: HTML content with proper Content-Type header

### Task 4: Environment Variable Support
- [ ] **Implementation**: Use `process.env.PORT || 3000` for port configuration
- [ ] **Default Behavior**: Still defaults to 3000 if PORT not set
- [ ] **Test Command**: `PORT=8080 npm start`
- [ ] **Expected**: Server runs on specified port

### Task 5: Request Logging
- [ ] **Implementation**: Log all incoming requests (method, URL, timestamp)
- [ ] **Format**: Should show what endpoints are being hit
- [ ] **Test Command**: Make requests and observe console output
- [ ] **Expected**: Each request logged with relevant details

## Verification Commands

```bash
# 1. Start the server
cd /home/james/test-simple-project
npm start

# 2. Test root endpoint (should return HTML)
curl -i http://localhost:3000/

# 3. Test status endpoint (should return JSON)
curl -i http://localhost:3000/status

# 4. Test custom port (in new terminal)
PORT=8080 npm start
curl -i http://localhost:8080/

# 5. Verify logging (check console output during requests)
```

## Success Criteria Checklist

- [ ] **Criterion 1**: Server starts without errors
- [ ] **Criterion 2**: /status endpoint returns valid JSON with timestamp
- [ ] **Criterion 3**: Root path (/) returns simple HTML page
- [ ] **Criterion 4**: Port configurable via PORT environment variable
- [ ] **Criterion 5**: Basic error handling prevents server crashes
- [ ] **Criterion 6**: Request logging shows activity

## Code Structure Expected

```javascript
const http = require('http');
const url = require('url');

// Environment variable support
const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  // Request logging
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

  try {
    const parsedUrl = url.parse(req.url, true);

    // Route handling
    if (parsedUrl.pathname === '/') {
      // HTML response
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end('<html><body><h1>Simple Test App</h1></body></html>');
    } else if (parsedUrl.pathname === '/status') {
      // JSON response
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({
        status: 'ok',
        timestamp: new Date().toISOString()
      }));
    } else {
      // 404 handling
      res.writeHead(404, {'Content-Type': 'text/plain'});
      res.end('Not Found');
    }
  } catch (error) {
    // Error handling
    console.error('Server error:', error);
    res.writeHead(500, {'Content-Type': 'text/plain'});
    res.end('Internal Server Error');
  }
});

// Error handling for server
server.on('error', (error) => {
  console.error('Server error:', error);
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
```

## Completion Status: 1/6 (17%) ❌

**Next Action**: Claude agent must implement all missing features and verify completion.