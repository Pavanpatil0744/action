const supertest = require('supertest');
https://capture.vkyc.hdfcbank.com/captures?t=XO5FqWyqhTDg
const app = require('../app');

const agent = supertest.agent(app);

describe('simple get request', () => {
  it('should return 200 ok', async () => {
    const response = await agent.get('/').send();
    expect(response.status).toEqual(200);
  });
});
