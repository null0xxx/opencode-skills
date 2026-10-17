# OpenCode V2 — ზუსტი skill/command კონფიგურაციის დაყენება (Windows)

შენ ხარ OpenCode აგენტი Windows-ის კომპიუტერზე. ამოცანა: ამ მანქანაზე ზუსტად ისე დააყენო გლობალური OpenCode V2 კონფიგურაცია, როგორც წყარო-მანქანაზეა დაყენებული — **57 skill, 57 command, `opencode.json` და `AGENTS.md`** — ერთი-ერთში, 100%.

**წყარო:** private რეპო `null0xxx/opencode-skills`, branch `main`.
**სამიზნე:** `%USERPROFILE%\.config\opencode\` (მოსალოდნელი მნიშვნელობა: `C:\Users\user\.config\opencode`).

## მკაცრი წესები

1. ყველა ფაილი კოპირდება **verbatim** — არაფერი "გააუმჯობესო", არაფერი წაშალო, არაფერი გადააკეთო. ერთადერთი დაშვებული ცვლილებაა ნაბიჯი 4-ის ბილიკების ჩანაცვლება.
2. თუ `%USERPROFILE%\.config\opencode` უკვე არსებობს — ჯერ backup გააკეთე (ნაბიჯი 3), და მხოლოდ მერე ჩაწერე.
3. ნაბიჯი 5-ის შემოწმებები სავალდებულოა. თუ რომელიმე არ გაივლის — გაჩერდი და მაცნობე ზუსტად რომელი.

## როგორ გამოიძახება skill-ები — `/` მენიუთი (ზუსტად როგორც წყარო-მანქანაზე)

- OpenCode-ის პრომპტის ველში აკრიფე `/` — გამოჩნდება **57 command**, თითო skill-ისთვის ერთი; command-ის სახელი ემთხვევა skill-ის ID-ს (მაგ. `/ultrawork`, `/git-master`, `/ulw-plan`, `/debugging`).
- `/ultrawork` (და სხვა) ჩატვირთავს შესაბამის skill-ს და შეასრულებს მოთხოვნას — ზუსტად როგორც წყარო-მანქანაზე.
- skill-ები ავტომატურადაც ჩაიტვირთება, თუ მოთხოვნა მათ ეხება; სურვილისამებრ შეგიძლია `@ultrawork` ფორმით მიუთითო პრომპტში.
- სწორედ ამას აკეთებს `commands\` საქაღალდის 57 `.md` ფაილი — **ისინი სავალდებულოა**; მათ გარეშე `/` მენიუ ცარიელი იქნება.
- ამ მანქანაზეც ზუსტად ასე გამოიძახებ: `/ultrawork`, `/programming`, `/debugging`, ... (სრული სია — `commands\` საქაღალდეში).

## ნაბიჯი 1 — OpenCode V2

- შეამოწმე: `opencode --version`
- თუ არ არის დაყენებული (Windows-ზე package manager-ები არ არის მხარდაჭერილი, standalone zip გამოიყენე):
  - x64: ჩამოტვირთე `https://opencode.ai/update/api/latest/cli/opencode/opencode-windows-x64.zip`
  - ARM64: `https://opencode.ai/update/api/latest/cli/opencode/opencode-windows-arm64.zip`
  - ამოაარქივე `%USERPROFILE%\.opencode\bin\`-ში, დაამატე ეს საქაღალდე PATH-ში, გახსენი ახალი ტერმინალი და გადაამოწმე `opencode --version`.
  - ალტერნატივა (თუ npm აყენია): `npm install -g @opencode/cli`

## ნაბიჯი 2 — წყაროს მიღება

- სასურველი გზა (რეპო private-ია):
  1. `gh auth login` — ანგარიში **null0xxx**
  2. `gh repo clone null0xxx/opencode-skills "$env:USERPROFILE\Documents\opencode-skills"`
- თუ `gh` არ არის: გადმოწერე `https://github.com/null0xxx/opencode-skills/archive/refs/heads/main.zip` (GitHub-ზე შესვლა ანგარიშით null0xxx) და ამოაარქივე `%USERPROFILE%\Documents\opencode-skills`-ში.
- ⚠️ თუ არსებობს ძველი `Documents\opencode-skills-main` საქაღალდე — **ის მოძველებულია, არ გამოიყენო**. აუცილებლად ახლიდან გადმოწერე/დაკლონე.
- გადაამოწმე წყარო: `skills\` უნდა შეიცავდეს **ზუსტად 57 საქაღალდეს**, `commands\` — **ზუსტად 57 `.md` ფაილს**. თუ რაოდენობა სხვაა — გაჩერდი და მაცნობე.

## ნაბიჯი 3 — backup და კოპირება

- თუ `%USERPROFILE%\.config\opencode` არსებობს: გადაარქვი სახელი → `%USERPROFILE%\.config\opencode.backup-<დღევანდელი თარიღი>`.
- შექმენი `%USERPROFILE%\.config\opencode` და დააკოპირე (სტრუქტურის შენარჩუნებით):
  - `skills\*` → `%USERPROFILE%\.config\opencode\skills\`
  - `commands\*.md` → `%USERPROFILE%\.config\opencode\commands\`
  - `config\opencode.json` → `%USERPROFILE%\.config\opencode\opencode.json`
  - `config\AGENTS.md` → `%USERPROFILE%\.config\opencode\AGENTS.md`

## ნაბიჯი 4 — ბილიკების ჩანაცვლება (ერთადერთი დაშვებული ცვლილება)

დააკოპირებულ ყველა ტექსტურ ფაილში (`skills/`, `commands/`, `opencode.json`, `AGENTS.md`) ჩაანაცვლე:

- `/home/secc` → `C:/Users/user`

(თუ `$env:USERPROFILE` არ არის `C:\Users\user`, გამოიყენე რეალური მნიშვნელობა forward slashes-ით, მაგ. `C:/Users/<name>`.)

ეს ფარავს ყველა აბსოლუტურ ბილიკს, მათ შორის:
`/home/secc/.config/opencode/skills/...`, `/home/secc/.config/opencode/skills/**`, `/home/secc/.opencode/bin/opencode`, `/home/secc/.local/share/opencode-skill-runtimes/...`.

## ნაბიჯი 5 — ვერიფიკაცია (ცხრილად მოახსენე)

- `skills` საქაღალდეების რაოდენობა = **57**  (`(Get-ChildItem "$env:USERPROFILE\.config\opencode\skills" -Directory).Count`)
- `commands` `.md` ფაილების რაოდენობა = **57**
- `SKILL.md` ფაილები, რომლებშიც არის `Installed OpenCode v2 compatibility` = **57**
- `SKILL.md` ფაილები, რომლებშიც არის `disable-model-invocation: true` = **28**
- ძებნა `findstr /s /m /c:"/home/secc"` კონფიგის საქაღალდეზე — **არაფერი** უნდა იპოვოს
- `opencode --version` მუშაობს; გაუშვი OpenCode; პრომპტის ველში აკრიფე `/` — უნდა გამოჩნდეს **57 command**; გამოსცადე `/ultrawork` — შესაბამისი skill უნდა ჩაიტვირთოს

## ნაბიჯი 6 — სურვილისამებრ (დაყენებისთვის სავალდებულო არ არის)

- ast-grep (Windows ბინარი; რეპოში განზრახ არ არის Linux-ის 51MB `bin/sg`):
  `powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.config\opencode\skills\ast-grep\install.ps1"`
- Node.js და Python 3 — ზოგი skill-ის დამხმარე სკრიპტებისთვის.
- browser skill — საჭიროა Chromium/Brave (სურვილისამებრ).
- OMO (oh-my-openagent) **არ არის საჭირო** — ეს skill-ები დამოუკიდებელი ინსტრუქციების პაკეტებია.
- `opencode.json`-ში `lmstudio` provider (127.0.0.1:1235) და მოდელი `opencode/longcat-2.5-preview-free` წყარო-მანქანის პარამეტრებია — შეგიძლია დატოვო ან შეცვალო.

## სად ვნახო?

- **ეს დოკუმენტი და ამოცანის მიმდინარეობა რეპოშია:** `main` branch-ის `INSTALL-PROMPT.md` (ასლი ავტორის Linux მანქანაზეცაა: `Documents/System/Workstation/opencode-skills-windows-install-prompt-2026-10-17.md`).
- **დაყენების შემდეგ, ამ მანქანაზე:**
  - ფაილები: `%USERPROFILE%\.config\opencode\` (skills • commands • opencode.json • AGENTS.md)
  - OpenCode-ში: აკრიფე `/` — უნდა ჩანდეს 57 command; skill-ის გამოძახება: `/ultrawork` (ან სხვა skill-ის ID)
  - ვერიფიკაცია: ნაბიჯი 5 (57 / 57 / 57 / 28)

## განახლება მომავალში

```powershell
cd "$env:USERPROFILE\Documents\opencode-skills"; git pull
# შემდეგ თავიდან დააკოპირე skills\ და commands\ .config\opencode\-ში და გაიმეორე ნაბიჯი 4
```

## დასკვნითი მოხსენება

დაწერე: რომელი ნაბიჯები შესრულდა, ნაბიჯი 5-ის 6 შემოწმების შედეგი, ყველა გადახრა (თუ იყო) და შექმნილი ბილიკები.
