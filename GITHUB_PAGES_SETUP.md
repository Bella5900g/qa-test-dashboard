# 🚀 Configuração do GitHub Pages

Este guia explica como configurar o GitHub Pages para hospedar a documentação do QA Test Dashboard.

## 📋 Pré-requisitos

- Repositório criado no GitHub: `https://github.com/Bella5900g/qa-test-dashboard`
- Acesso de administrador ao repositório

## ⚙️ Configuração Passo a Passo

### 1. **Habilitar GitHub Pages**

1. Acesse o repositório no GitHub
2. Vá em **Settings** (Configurações)
3. Role até a seção **Pages** no menu lateral
4. Em **Source**, selecione **Deploy from a branch**
5. Em **Branch**, selecione **main** e pasta **/ (root)**
6. Clique em **Save**

### 2. **Configurar GitHub Actions (Opcional)**

O arquivo `.github/workflows/deploy.yml` já está configurado para:
- Executar testes automaticamente
- Fazer deploy da documentação
- Atualizar o site a cada push na branch main

### 3. **Estrutura de Arquivos**

```
qa-test-dashboard/
├── docs/
│   └── index.html          # Página principal da documentação
├── frontend/               # Código do dashboard
├── backend/                # API Flask
├── README.md              # Documentação principal
├── _config.yml            # Configuração do Jekyll
└── .github/workflows/     # GitHub Actions
```

## 🌐 URLs de Acesso

Após a configuração, o site estará disponível em:

- **Documentação**: `https://bella5900g.github.io/qa-test-dashboard/`
- **Dashboard**: `https://bella5900g.github.io/qa-test-dashboard/` (mesma URL)
- **Repositório**: `https://github.com/Bella5900g/qa-test-dashboard`

## 🔧 Personalização

### Alterar Tema/Cores

Edite o arquivo `docs/index.html` e modifique as variáveis CSS:

```css
:root {
    --primary-color: #6f42c1;    /* Cor principal */
    --secondary-color: #6c757d;  /* Cor secundária */
    --success-color: #28a745;    /* Cor de sucesso */
    --info-color: #17a2b8;       /* Cor de informação */
    --warning-color: #ffc107;    /* Cor de aviso */
    --danger-color: #dc3545;     /* Cor de erro */
}
```

### Adicionar Novas Páginas

1. Crie novos arquivos HTML na pasta `docs/`
2. Adicione links na navegação do `index.html`
3. Faça commit e push das alterações

### Atualizar Informações Pessoais

Edite as seguintes seções no `docs/index.html`:

- **Seção Developer** (linha ~200)
- **Seção Contact** (linha ~300)
- **Footer** (linha ~350)

## 📊 Métricas e Analytics

### Google Analytics (Opcional)

Para adicionar Google Analytics, insira o código de tracking no `<head>` do `docs/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### GitHub Insights

O GitHub automaticamente rastreia:
- Visualizações do repositório
- Clones
- Tráfego do GitHub Pages
- Stars e Forks

## 🚀 Deploy Automático

O GitHub Actions está configurado para:

1. **Executar testes** a cada push
2. **Fazer build** da documentação
3. **Deploy automático** para GitHub Pages
4. **Notificações** de status

### Verificar Status do Deploy

1. Vá em **Actions** no repositório
2. Verifique o status do workflow "Deploy to GitHub Pages"
3. Clique no workflow para ver logs detalhados

## 🔍 Troubleshooting

### Site não carrega

1. Verifique se o GitHub Pages está habilitado
2. Confirme se a branch está correta (main)
3. Aguarde alguns minutos para propagação

### Erro 404

1. Verifique se o arquivo `docs/index.html` existe
2. Confirme se o caminho está correto
3. Verifique os logs do GitHub Actions

### CSS não carrega

1. Verifique se os CDNs estão acessíveis
2. Confirme se os caminhos dos arquivos estão corretos
3. Teste localmente antes do deploy

## 📱 Responsividade

O site foi desenvolvido com:
- **Bootstrap 5** para responsividade
- **Mobile-first** design
- **Touch-friendly** interface
- **Cross-browser** compatibility

## 🔒 Segurança

- **HTTPS** automático do GitHub Pages
- **Content Security Policy** configurado
- **No dados sensíveis** no código
- **Dependências** atualizadas

## 📈 SEO

O site inclui:
- **Meta tags** otimizadas
- **Open Graph** para redes sociais
- **Schema.org** markup
- **Sitemap** automático
- **URLs** amigáveis

## 🎯 Próximos Passos

1. **Personalizar** cores e conteúdo
2. **Adicionar** mais páginas de documentação
3. **Configurar** analytics
4. **Otimizar** performance
5. **Adicionar** testes automatizados

---

## 📞 Suporte

Para dúvidas ou problemas:

- **Email**: bellacandy5900g@gmail.com
- **LinkedIn**: [linkedin.com/in/isabellavieiraqa](https://www.linkedin.com/in/isabellavieiraqa/)
- **GitHub**: [github.com/bella5900g](https://github.com/bella5900g)

---

**💡 Dica**: Mantenha o repositório atualizado e faça commits regulares para manter o site sempre atualizado!
