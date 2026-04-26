# Skill: 创建 Ent Schema

## 描述
为 welogin 项目创建新的数据库实体 (Ent Schema)。

## 触发词
- "创建实体"
- "添加数据库表"
- "新建 schema"
- "定义模型"

## 步骤

### 1. 创建 Schema 文件
使用 Task 命令创建基础 schema：

```bash
task db:ent:new -- YourEntity
```

或手动在 `schemas/weloginschema/` 创建：

```go
package weloginschema

import (
    "time"

    "entgo.io/ent"
    "entgo.io/ent/schema/field"
    "entgo.io/ent/schema/index"
    "entgo.io/ent/schema/edge"
    "github.com/pubgo/welogin/pkg/entmixins"
)

type YourEntity struct {
    ent.Schema
}

func (YourEntity) Mixin() []ent.Mixin {
    return []ent.Mixin{
        entmixins.SoftDelete{},  // 软删除支持
    }
}

func (YourEntity) Fields() []ent.Field {
    return []ent.Field{
        field.String("id").
            Unique().
            Immutable().
            Comment("主键 ID"),
        field.String("name").
            NotEmpty().
            Comment("名称"),
        field.Time("created_at").
            Default(time.Now).
            Immutable().
            Comment("创建时间"),
        field.Time("updated_at").
            Default(time.Now).
            UpdateDefault(time.Now).
            Comment("更新时间"),
    }
}

func (YourEntity) Edges() []ent.Edge {
    return []ent.Edge{
        // 关联到 Account
        edge.From("account", Account.Type).
            Ref("your_entities").
            Unique().
            Required(),
    }
}

func (YourEntity) Indexes() []ent.Index {
    return []ent.Index{
        index.Fields("name"),
    }
}
```

### 2. 生成代码
```bash
task db:ent:gen
```

### 3. 更新数据库
```bash
# 查看将要执行的 SQL
task db:schema:diff

# 执行数据库迁移
task db:schema:create
```

## 常用字段类型

```go
field.String("name")           // 字符串
field.Int("count")             // 整数
field.Bool("active")           // 布尔
field.Time("created_at")       // 时间
field.Enum("status").Values()  // 枚举
field.JSON("metadata", map[string]any{})  // JSON
field.Bytes("data")            // 二进制
```

## 常用验证

```go
field.String("email").
    NotEmpty().
    Match(regexp.MustCompile(`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`))

field.Int("age").
    Positive().
    Max(150)
```

## 软删除 Mixin
项目已提供 `entmixins.SoftDelete`，会自动添加 `deleted_at` 字段和过滤逻辑。
