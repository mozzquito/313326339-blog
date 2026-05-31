import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://313326339.xyz',
  integrations: [mdx()],
});
