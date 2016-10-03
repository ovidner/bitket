angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/cart.main.html",'<div layout="row" layout-sm="column"><md-content layout-padding="" flex-gt-sm="50"><h2>Kundvagn</h2><table flex="" width="100%"><tr ng-repeat="holding in ctrl.cart.holdings"><td><md-button class="md-icon-button md-warn" ng-click="ctrl.deleteHolding(holding)"><md-icon>delete</md-icon></md-button></td><td align="left">{{holding.product_name}}</td><td align="right">{{holding.price | currency}}</td></tr><tr><td></td><td align="left">Totalt:</td><td align="right">{{ctrl.cart.total | currency}}</td></tr></table><h2>Köpinformation</h2><p>Evenemangsbiljetter levereras direkt vid köpet på elektronisk väg och kan därför <em>inte återköpas</em>.</p><p>Betalningen går automatiskt direkt till arrangören eller arrangörerna.</p></md-content><md-content layout-padding="" flex-gt-sm="50"><h2>Betalningsuppgifter</h2><form name="cardForm"><div layout="row" layout-sm="column" layout-fill=""><md-input-container flex=""><label>Kortnummer</label> <input cc-number="" cc-format="" name="number" ng-model="ctrl.card.number" required="" novalidate=""></md-input-container></div><div layout="row" layout-sm="column" layout-fill=""><md-input-container flex=""><label>Giltigt till (månad)</label> <input cc-exp-month="" name="expMonth" ng-model="ctrl.card.exp_month" required=""></md-input-container><md-input-container flex=""><label>Giltigt till (år)</label> <input cc-exp-year="" name="expYear" ng-model="ctrl.card.exp_year" required=""></md-input-container><md-input-container flex=""><label>CVV/CVC</label> <input cc-cvc="" name="cvc" ng-model="ctrl.card.cvc" required=""></md-input-container></div></form><p>Betalningen sker med hjälp av <a href="https://stripe.com/se" target="_blank">Stripe</a>. Dina kortuppgifter lagras aldrig hos varken Liubiljett eller arrangören.</p><div layout="row"><span flex=""></span><md-button class="md-raised md-primary" ng-click="ctrl.purchase()" ng-disabled="cardForm.$invalid || ctrl.purchaseProgress.status === \'working\' || ctrl.purchaseProgress.status === \'succeeded\'">Genomför köp</md-button></div></md-content></div>')}]);
angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/holding.detail.main.html",'<div><h1>{{ctrl.holding.product_name}}</h1><img ng-src="{{ctrl.holding.url}}qr/" style="width: 100%; max-width: 225px;"><p ng-if="ctrl.holding.utilized"><strong style="color: red;">Utnyttjad {{ctrl.holding.utilized | date:\'medium\'}}.</strong></p><p ng-if="!ctrl.holding.utilized"><strong style="color: green;">Ej utnyttjad.</strong></p><md-button class="md-raised md-primary" ng-if="ctrl.holding.permissions.utilize && !ctrl.holding.utilized" ng-click="ctrl.holding.utilize()">Markera som utnyttjad</md-button><md-button class="md-raised md-warn" ng-if="ctrl.holding.permissions.unutilize && ctrl.holding.utilized" ng-click="ctrl.holding.unutilize()">Markera som ej utnyttjad</md-button><p><small>Biljett-id: {{ctrl.holding.id}}</small></p><p>Vem som helst som har adressen till den här sidan, QR-koden eller biljett-id:t kan använda den här biljetten. Därför är det mycket viktigt att du skyddar dessa saker från obehöriga. Liubiljett eller arrangören tar inget ansvar för förlorade eller spridda biljetter.</p></div>')}]);
angular.module("tickle").run(["$templateCache",function(i){i.put("/static/templates/holding.utilize.main.html",'<div><div layout="row" layout-fill=""><form ng-submit="ctrl.submit()"><md-input-container flex=""><label>LiU-kortnummer</label> <input name="liuCard" ng-model="ctrl.queryParams.liu_card"></md-input-container><md-input-container flex=""><label>LiU-id</label> <input name="liuId" ng-model="ctrl.queryParams.liu_id"></md-input-container><md-input-container flex=""><label>Biljettnummer</label> <input name="holdingId" ng-model="ctrl.queryParams.id"></md-input-container><md-button class="md-raised" ng-click="ctrl.submit()"><md-icon>search</md-icon>Sök</md-button></form></div><md-progress-circular md-mode="indeterminate" ng-if="ctrl.loading"></md-progress-circular><md-card ng-repeat="holding in ctrl.holdings"><md-card-content><h2 class="md-title">{{holding.product_name}}</h2><p>Biljettnummer: {{holding.id}}</p></md-card-content><div class="md-actions" layout="row" layout-align="end center"><span ng-if="holding.utilized">Utlämnad {{holding.utilized | date:\'medium\'}}</span><md-button class="md-raised md-warn" ng-if="holding.utilized" ng-click="holding.unutilize()">Lämna tillbaka</md-button><md-button class="md-raised md-primary" ng-if="!holding.utilized" ng-click="holding.utilize()">Lämna ut</md-button></div></md-card></div>')}]);
angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/home.main.html","<h2>liubiljett.se</h2><p>Välkommen till liubiljett.se! Här säljs biljetter till studentevenemang på Linköpings universitet.</p><p>I menyn till vänster kan du välja vilket evenemang du vill köpa biljett till.</p><p>Tjänsten är fortfarande ny och drivs med en mycket begränsad budget. Därför kan saker ibland gå lite långsamt. Tack för ditt tålamod!</p><h3>Viktig information om cookies</h3><p>Denna webbsida kräver cookies för att kunna fungera. Genom att fortsätta använda tjänsten godkänner du att cookies lagras på din dator.</p>")}]);
angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/organizer.event.main.html",'<h1>{{ctrl.event.name}}</h1><div marked="ctrl.event.description"></div><div layout="row" layout-wrap=""><div ng-repeat="product in ctrl.event.products track by $index" flex-sm="100" flex-md="50" flex-gt-md="50" flex-gt-lg="33"><lb-product-card product="product"></lb-product-card></div></div>')}]);
angular.module("tickle").run(["$templateCache",function(i){i.put("/static/templates/directives/lb-person-menu.html",'<md-list-item class="md-2-line" ng-if="person"><md-icon class="md-avatar-icon">person</md-icon><div class="md-list-item-text" layout="column"><h3>{{person.first_name}} {{person.last_name}}</h3><p>{{person.email}}</p></div></md-list-item><md-list-item ng-if="person" ui-sref="liubiljett.cart"><md-icon class="md-avatar-icon">shopping_cart</md-icon><p>Kundvagn</p></md-list-item><md-list-item ng-if="person" ui-sref="liubiljett.auth.logout"><md-icon class="md-avatar-icon">power_settings_new</md-icon><p>Logga ut</p></md-list-item><md-list-item ng-if="!person" ng-click="openLoginDialog()"><md-icon class="md-avatar-icon">power_settings_new</md-icon><p>Logga in/Skapa konto</p></md-list-item>')}]);
angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/directives/lb-product-card.html",'<form name="productForm"><md-card layout-padding=""><md-card-content layout="column"><h3 class="md-title">{{ctrl.product.name}}</h3><div marked="ctrl.product.description"></div><md-input-container flex="" ng-repeat="variation in ctrl.product.variations"><label>{{variation.name}}</label><md-select placeholder="Välj dryck" ng-model="variation.getSetSelectedChoice" ng-model-options="{getterSetter: true}" required=""><md-option ng-repeat="choice in variation.choices" ng-value="choice">{{choice.name}} <span class="md-caption" ng-if="choice.delta_amount != 0">({{choice.delta_amount | currency}})</span></md-option></md-select></md-input-container></md-card-content><md-card-footer layout="column"><div layout="row"><span class="md-body-1" flex="">Grundpris</span> <span class="md-body-1" layout-align="right">{{ctrl.product.base_price | currency}}</span></div><div layout="row" ng-repeat="variation in ctrl.product.variations"><span class="md-body-1" flex="">{{variation.name}}: {{variation.selectedChoice.name}} <i ng-if="!variation.selectedChoice">Inte valt</i></span> <span class="md-body-1" layout-align="right">{{variation.selectedChoice.delta_amount | currency}}</span></div><div layout="row" ng-repeat="modifier in ctrl.product.modifiers"><span class="md-body-1" flex="">{{modifier.condition}}</span> <span class="md-body-1" layout-align="right">{{modifier.delta_amount | currency}}</span></div><md-divider></md-divider><div layout="row"><span class="md-body-2" flex="">Ditt pris</span> <span class="md-body-2" layout-align="right">{{ctrl.product.price | currency}}</span></div><p ng-if="!ctrl.loggedIn">För att kunna visa rätt priser och rätt information behöver du logga in för att fortsätta. Det gör du i menyn till vänster.</p></md-card-footer><div class="md-actions" layout="row" layout-align="end center"><md-button class="md-raised md-accent" ng-click="ctrl.addToCart()" ng-disabled="productForm.$invalid || !ctrl.loggedIn"><md-icon>add_shopping_cart</md-icon>Lägg i kundvagn</md-button></div></md-card></form>')}]);
angular.module("tickle").run(["$templateCache",function(i){i.put("/static/templates/partials/loginDialog.html",'<md-dialog aria-label="Logga in"><md-dialog-content class="md-dialog-content"><div layout="row" layout-sm="column" layout-padding=""><div><h2>LiU-id</h2><p>För att kunna få eventuell kårrabatt måste du logga in med LiU-id.</p><md-button class="md-raised md-primary" ui-sref="liubiljett.auth.login.liu">Logga in med LiU-id</md-button></div><div><h2>Facebook</h2><p>Logga in med Facebook om du inte är student eller anställd på LiU.</p><md-button class="md-raised md-primary" ui-sref="liubiljett.auth.login.facebook">Logga in med Facebook</md-button></div></div></md-dialog-content><md-dialog-actions class="md-actions"><md-button ng-click="dialog.hide()">Stäng</md-button></md-dialog-actions></md-dialog>')}]);
angular.module("tickle").run(["$templateCache",function(t){t.put("/static/templates/partials/purchaseProgressDialog.html",'<md-dialog aria-label="Genomför köp..."><md-dialog-content class="md-dialog-content"><div ng-if="dialog.progress.status === \'working\'"><div layout="column" layout-align="start center"><h2>Genomför köp...</h2><md-progress-circular md-mode="indeterminate"></md-progress-circular></div><p>Ditt köp bearbetas. Undvik att stänga eller ladda om sidan.</p></div><div ng-if="dialog.progress.status === \'failed\'"><p>Köpet misslyckades av följande skäl: {{dialog.progress.statusMessage}}</p></div><div ng-if="dialog.progress.status === \'succeeded\'"><div layout="column" layout-align="start center"><h2>Klart!</h2></div><p>Ditt biljettköp är klart. Kvitto på betalningen samt mer information om din biljett kommer per mail.</p><p>Ha det fint!</p></div></md-dialog-content><md-dialog-actions class="md-actions"><md-button ng-click="dialog.hide()" ng-if="dialog.progress.status !== \'working\'">Stäng</md-button></md-dialog-actions></md-dialog>')}]);