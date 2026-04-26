# Skill: 创建前端功能模块

## 描述
为 welogin 前端创建新的功能模块。

## 触发词
- "创建前端功能"
- "添加页面"
- "新建组件"
- "前端模块"

## 项目结构

```
frontend/src/
├── features/           # 功能模块
│   └── your-feature/
│       ├── components/ # 模块专用组件
│       ├── hooks/      # 自定义 hooks
│       ├── api.ts      # API 调用
│       └── index.ts    # 导出
├── components/ui/      # shadcn/ui 组件
├── pages/              # 页面组件
├── store/              # Zustand 状态
└── gen/                # protobuf 生成代码
```

## 步骤

### 1. 生成 TypeScript Proto 代码
```bash
task proto:gen:ts
# 或
cd frontend && pnpm run gen:proto
```

### 2. 创建 API 调用层

```typescript
// frontend/src/features/your-feature/api.ts
import { GrpcWebFetchTransport } from "@protobuf-ts/grpcweb-transport";
import { YourServiceClient } from "../../gen/welogin/v1/your_service.client";

const transport = new GrpcWebFetchTransport({
  baseUrl: import.meta.env.VITE_API_URL || "http://localhost:8080",
});

export const yourServiceClient = new YourServiceClient(transport);

export async function yourMethod(params: { name: string }) {
  const { response } = await yourServiceClient.yourMethod({
    name: params.name,
  });
  return response;
}
```

### 3. 创建 Zustand Store

```typescript
// frontend/src/store/your-store.ts
import { create } from "zustand";

interface YourState {
  data: YourData | null;
  loading: boolean;
  error: string | null;
  fetchData: () => Promise<void>;
}

export const useYourStore = create<YourState>((set) => ({
  data: null,
  loading: false,
  error: null,
  fetchData: async () => {
    set({ loading: true, error: null });
    try {
      const data = await yourMethod();
      set({ data, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
}));
```

### 4. 创建组件

```tsx
// frontend/src/features/your-feature/components/YourComponent.tsx
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useYourStore } from "@/store/your-store";

export function YourComponent() {
  const { data, loading, error, fetchData } = useYourStore();

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Feature</CardTitle>
      </CardHeader>
      <CardContent>
        {/* 内容 */}
      </CardContent>
    </Card>
  );
}
```

### 5. 添加路由

```tsx
// frontend/src/router.tsx
import { YourPage } from "./pages/YourPage";

export const router = createBrowserRouter([
  // ...existing routes
  {
    path: "/your-feature",
    element: <YourPage />,
  },
]);
```

## shadcn/ui 组件使用

项目已配置 shadcn/ui，常用组件：

```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
```

## 开发命令

```bash
cd frontend
pnpm dev      # 开发服务器
pnpm build    # 构建
pnpm lint     # 类型检查
```
