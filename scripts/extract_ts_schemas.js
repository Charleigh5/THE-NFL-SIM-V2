const fs = require('fs');
const path = require('path');
const ts = require(path.resolve('frontend/node_modules/typescript'));

const docsDir = path.resolve('docs/design_theory/nfl_simulation_blueprint');
const files = ['physics_engine.md', 'dynasty_empire.md', 'broadcast_director.md', 'ui_design_system.md'];

function extractCodeBlocks(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const regex = /```(\w+)?\r?\n([\s\S]*?)```/g;
  const blocks = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    blocks.push({
      lang: match[1] || 'none',
      code: match[2]
    });
  }
  return blocks;
}

function parseTypeScriptCode(code, sourceFileName) {
  const sourceFile = ts.createSourceFile(
    sourceFileName,
    code,
    ts.ScriptTarget.ES2022,
    true,
    ts.ScriptKind.TS
  );

  const result = {
    interfaces: {},
    types: {},
    enums: {},
    constObjects: {},
    anyUsages: []
  };

  function visit(node) {
    // Check for `any` type keyword
    if (node.kind === ts.SyntaxKind.AnyKeyword) {
      const { line, character } = sourceFile.getLineAndCharacterOfPosition(node.getStart());
      result.anyUsages.push({
        line: line + 1,
        character: character + 1,
        snippet: node.getText(sourceFile)
      });
    }

    if (ts.isInterfaceDeclaration(node)) {
      const name = node.name.text;
      const properties = {};
      node.members.forEach(member => {
        if (ts.isPropertySignature(member)) {
          const propName = member.name.getText(sourceFile);
          const isOptional = !!member.questionToken;
          const typeText = member.type ? member.type.getText(sourceFile).trim() : 'implicit_any';
          properties[propName] = {
            type: typeText,
            optional: isOptional
          };
        }
      });
      result.interfaces[name] = {
        name,
        properties
      };
    } else if (ts.isTypeAliasDeclaration(node)) {
      const name = node.name.text;
      const typeText = node.type.getText(sourceFile).trim();
      result.types[name] = {
        name,
        type: typeText
      };
    } else if (ts.isEnumDeclaration(node)) {
      const name = node.name.text;
      const members = {};
      node.members.forEach(member => {
        const memName = member.name.getText(sourceFile);
        const memVal = member.initializer ? member.initializer.getText(sourceFile) : memName;
        members[memName] = memVal;
      });
      result.enums[name] = {
        name,
        members
      };
    } else if (ts.isVariableStatement(node)) {
      node.declarationList.declarations.forEach(decl => {
        if (ts.isIdentifier(decl.name) && decl.initializer && ts.isAsExpression(decl.initializer)) {
          const name = decl.name.text;
          const expr = decl.initializer.expression;
          if (ts.isObjectLiteralExpression(expr)) {
            const properties = {};
            expr.properties.forEach(prop => {
              if (ts.isPropertyAssignment(prop)) {
                properties[prop.name.getText(sourceFile)] = prop.initializer.getText(sourceFile);
              }
            });
            result.constObjects[name] = {
              name,
              properties
            };
          }
        }
      });
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
  return result;
}

const allTsSchemas = {};

files.forEach(fname => {
  const fpath = path.join(docsDir, fname);
  const blocks = extractCodeBlocks(fpath);
  allTsSchemas[fname] = [];

  blocks.forEach((block, idx) => {
    if (block.lang === 'typescript') {
      const parsed = parseTypeScriptCode(block.code, `${fname}_block_${idx}.ts`);
      allTsSchemas[fname].push({
        blockIndex: idx,
        parsed
      });
    }
  });
});

console.log(JSON.stringify(allTsSchemas, null, 2));
